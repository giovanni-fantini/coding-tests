# frozen_string_literal: true

require 'csv'

module Commands
  class ParseUnitPrices
    def self.call(input:)
      new(input).call
    end

    def initialize(input)
      @input = input
      @unit_prices = {}
    end

    def call
      parse_unit_prices(input)
      unit_prices
    end

    private

    attr_reader :input
    attr_accessor :unit_prices

    def parse_unit_prices(input)
      CSV.read(input, headers: true, col_sep: '|',
                      header_converters: ->(f) { f.strip.downcase },
                      converters: ->(f) { f ? f.strip : nil })
         .each do |line|
        item_type = line['item']
        price = line['price'].gsub('£', '').to_i

        unit_prices[item_type] = price
      end
    end
  end
end
