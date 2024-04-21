# frozen_string_literal: true

module Commands
  class ParseDiscounts
    RECOGNIZED_DISCOUNTS = {
      'bundle_price' => /\W?\s?(\d+) items ([a-zA-z]+) for £(\d+)/,
      'percent_off_basket' => /(\d+)% off total basket cost\s?(for baskets worth over £\d+)?/
    }.freeze

    def self.call(input:)
      new(input).call
    end

    def initialize(input)
      @input = input
      @discounts = {}
    end

    def call
      parse_discounts(input)
      discounts
    end

    private

    attr_reader :input
    attr_accessor :discounts

    def parse_discounts(input)
      File.open(input).each_line do |line|
        RECOGNIZED_DISCOUNTS.each_pair do |discount, regex|
          match_data = regex.match(line)
          add_discount(discount, match_data) if match_data
        end
      end
    end

    def add_discount(discount, match_data)
      case discount
      when 'bundle_price'
        build_bundle_price_discount(match_data)
      when 'percent_off_basket'
        build_percent_off_basket_discount(match_data)
      end
    end

    def build_bundle_price_discount(match_data)
      discount = {
        item_quantity: match_data[1].to_i,
        item_type: match_data[2],
        bundle_price: match_data[3].to_i
      }

      discounts[:bundle_price] ||= []
      discounts[:bundle_price] << discount
    end

    def build_percent_off_basket_discount(match_data)
      percent_off = match_data[1].to_i
      minimum_spend = /\d+/.match(match_data[2])[0].to_i

      discounts[:percent_off_basket] ||= {}
      discounts[:percent_off_basket][minimum_spend] = percent_off
    end
  end
end
