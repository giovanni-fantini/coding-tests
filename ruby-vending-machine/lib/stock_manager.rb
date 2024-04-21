# frozen_string_literal: true

module VendingMachine
  class InvalidStockTypeError < StandardError; end

  class StockManager
    ACCEPTED_TYPES = %i[products coins].freeze

    def self.load(stock_type:, computer:)
      new(stock_type, computer).load
    end

    def self.restock(stock_type:, computer:)
      new(stock_type, computer).restock
    end

    def initialize(stock_type, computer)
      raise InvalidStockTypeError unless ACCEPTED_TYPES.include?(stock_type)

      @stock_type = stock_type
      @computer = computer
    end

    def load
      continue = 'Y'

      continue = add_item_from_input(stock_type) while continue == 'Y'
    end

    def restock
      if display.restock_existing?(stock_type)
        restock_existing(eval(stock_type.to_s)) # rubocop:disable Security/Eval
      else
        load
      end
    end

    private

    attr_reader :computer, :stock_type

    def add_item_from_input(stock_type)
      stock_type == :products ? add_product : add_coin
    rescue VendingMachine::InvalidCoinError,
           VendingMachine::InvalidProductError,
           VendingMachine::InvalidItemStockError => e
      display.output_error(e)
      'Y'
    end

    def add_product
      input = display.ask_product_info
      product = Product.new(name: input[:name], price: input[:price])
      products << ItemStock.new(item: product, quantity: input[:quantity])
      input[:continue]
    end

    def add_coin
      input = display.ask_coin_info(accepted_coins)
      coin = Coin.new(value: input[:value])
      coins << ItemStock.new(item: coin, quantity: input[:quantity])
      input[:continue]
    end

    def restock_existing(items)
      item_to_restock = display.get_list_input(items)
      quantity = display.ask_restock_quantity(item_to_restock.item.name)
      item_to_restock.restock(quantity)
    end

    def display
      computer.display
    end

    def products
      computer.products
    end

    def coins
      computer.coins
    end

    def accepted_coins
      Coin.accepted_coins
    end
  end
end
