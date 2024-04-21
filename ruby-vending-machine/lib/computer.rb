# frozen_string_literal: true

module VendingMachine
  class Computer
    AVAILABLE_ACTIONS = %w[
      list_products
      buy_product
      restock_products
      restock_coins
      exit
    ].freeze

    attr_reader :display
    attr_accessor :products, :coins

    def self.run
      new.run
    end

    def initialize
      @display = UserDisplay.new
      @products = []
      @coins = []
    end

    def run # rubocop:disable Metrics/MethodLength
      take_initial_load
      user_choice = nil

      loop do
        begin
          display.clear_screen
          list_actions
          user_choice = display.get_list_input(AVAILABLE_ACTIONS)
          break if user_choice == 'exit'

          send(user_choice)
          display.pause
        rescue InvalidSelectionError
          display.invalid_selection
          display.pause
        end
      end
    end

    private

    def take_initial_load
      StockManager.load(stock_type: :products, computer: self)
      StockManager.load(stock_type: :coins, computer: self)
    end

    def list_actions
      display.list(AVAILABLE_ACTIONS, :actions)
    end

    def list_products
      display.list(products, :products)
    end

    def list_coins
      display.list(coins, :coins)
    end

    def buy_product
      list_products
      TransactionManager.buy_product(computer: self)
    end

    def restock_products
      list_products
      StockManager.restock(stock_type: :products, computer: self)
    end

    def restock_coins
      list_coins
      StockManager.restock(stock_type: :coins, computer: self)
    end

    def accepted_coins
      Coins.accepted_coins
    end
  end
end
