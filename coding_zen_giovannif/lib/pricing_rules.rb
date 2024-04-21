# frozen_string_literal: true

class PricingRules
  attr_reader :unit_prices, :discounts

  def initialize(unit_prices:, discounts: nil)
    @unit_prices = unit_prices
    @discounts = discounts
  end

  def find_discount_by_item_type(item_type)
    discounts[:bundle_price].each do |hash|
      return hash if hash[:item_type] == item_type
    end
    nil
  end

  def find_best_basket_discount(total)
    discounts[:percent_off_basket].select { |k, _v| total > k }
                                  .max_by { |_k, v| v }&.last
  end
end
