# frozen_string_literal: true

module Commands
  class CalculateTotal
    def self.call(pricing_rules:, basket:)
      new(pricing_rules, basket).call
    end

    def initialize(pricing_rules, basket)
      @pricing_rules = pricing_rules
      @basket = basket
      @totals = {
        grand_total: 0
      }
    end

    def call
      calculate_totals_pre_basket_discount
      apply_basket_discount
      totals[:grand_total]
    end

    private

    attr_reader :pricing_rules, :basket
    attr_accessor :totals

    def calculate_totals_pre_basket_discount
      basket.each_pair do |item_type, quantity|
        totals[item_type] = calculate_price_for_items(quantity, item_type)
        totals[:grand_total] += totals[item_type]
      end
    end

    def calculate_price_for_items(quantity, item_type)
      item_pricing = discount_pricing(item_type) || normal_pricing(item_type)

      price = (quantity / item_pricing[:quantity]) * item_pricing[:price]
      price += (quantity % item_pricing[:quantity]) * normal_pricing(item_type)[:price]
    end

    def discount_pricing(item_type)
      discount = pricing_rules.find_discount_by_item_type(item_type)
      return unless discount

      {
        price: discount[:bundle_price],
        quantity: discount[:item_quantity]
      }
    end

    def normal_pricing(item_type)
      {
        price: pricing_rules.unit_prices[item_type],
        quantity: 1
      }
    end

    def basket_discount(total)
      pricing_rules.find_best_basket_discount(total)
    end

    def apply_basket_discount
      if basket_discount(totals[:grand_total])
        percent_off = basket_discount(totals[:grand_total]) / 100.to_f

        totals[:grand_total] = totals[:grand_total] * (1 - percent_off)
      end
    end
  end
end
