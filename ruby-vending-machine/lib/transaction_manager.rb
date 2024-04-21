# frozen_string_literal: true

module VendingMachine
  class TransactionManager
    attr_reader :computer

    def self.buy_product(computer:)
      new(computer).buy_product
    end

    def initialize(computer)
      @computer = computer
    end

    def buy_product
      @desired_product = display.get_list_input(products)
      @price = @desired_product.item.price
      money = display.ask_money(@price, accepted_coins)
      return if money == 'C'

      @money = money.to_f
      check_funds_against_price
    rescue VendingMachine::InvalidSelectionError
      display.invalid_selection
      buy_product
    end

    private

    def check_funds_against_price
      if @money > @price
        issue_product_and_change
      elsif @money == @price
        issue_product
      else
        ask_more_money
      end
    end

    def issue_product_and_change
      ChangeManager.determine_and_issue(money: @money, price: @price, transaction_manager: self)
      issue_product
    end

    def issue_product
      @desired_product.release
      display.issue_product(@desired_product.item.name)
    rescue VendingMachine::EmptyStockError => e
      display.output_error(e)
    end

    def ask_more_money
      while @money < @price
        display.insufficient_funds
        price_difference = @price - @money
        difference = display.ask_money(price_difference, accepted_coins)
        return if difference == 'C'

        difference = difference.to_f
        @money = @money += difference
      end

      issue_product_and_change
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
