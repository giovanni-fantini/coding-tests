require 'pry-byebug'
require 'require_all'

require_relative 'lib/checkout'
require_relative 'lib/pricing_rules'
require_all 'lib/commands'

unit_prices = Commands::ParseUnitPrices.call(input: ARGV[0])
discounts = Commands::ParseDiscounts.call(input: ARGV[1])
basket = Commands::ParseBasket.call(input: ARGV[2])

pricing_rules = PricingRules.new(unit_prices: unit_prices, discounts: discounts)

checkout = Checkout.new(pricing_rules: pricing_rules)
checkout.scan_multiple(basket)
puts "Total is: #{checkout.total}"