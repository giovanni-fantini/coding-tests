# frozen_string_literal: true

module VendingMachine
  class InvalidProductError < StandardError; end
  class Product
    attr_reader :name, :price

    def initialize(name:, price:)
      @name = name
      unless price.is_a?(Float) && price.positive?
        raise InvalidProductError, "the provided price for product #{name} is not a valid non-zero decimal"
      end

      @price = price
    end
  end
end
