# frozen_string_literal: true

module VendingMachine
  class EmptyStockError < StandardError; end
  class InvalidItemStockError < StandardError; end

  class ItemStock
    attr_reader :item, :quantity

    def initialize(item:, quantity:)
      @item = item
      unless quantity.is_a?(Integer) && quantity.positive?
        raise InvalidItemStockError, "the provided quantity for item #{item.name} is not a valid non-zero integer"
      end

      @quantity = quantity
    end

    def release
      raise VendingMachine::EmptyStockError, "item #{@name} is out of stock" if @quantity.zero?

      @quantity -= 1
    end

    def restock(quantity)
      @quantity += quantity
    end
  end
end
