# frozen_string_literal: true

class Checkout
  attr_reader :pricing_rules, :basket

  def initialize(pricing_rules:)
    @pricing_rules = pricing_rules
    @basket = {}
  end

  def scan(item_type)
    unless unit_price(item_type)
      puts "Invalid item #{item_type}, please try again"
      end

    basket[item_type] ||= 0
    basket[item_type] += 1
  end

  def scan_multiple(items)
    items.each do |item_type|
      scan(item_type)
    end
  end

  def total
    Commands::CalculateTotal.call(pricing_rules: pricing_rules, basket: basket)
  end

  private

  def unit_price(item_type)
    pricing_rules.unit_prices[item_type]
  end
end
