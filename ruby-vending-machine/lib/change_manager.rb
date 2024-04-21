# frozen_string_literal: true

module VendingMachine
  class ChangeManager
    def self.determine_and_issue(money:, price:, transaction_manager:)
      new(money, price, transaction_manager).determine_and_issue
    end

    def initialize(money, price, transaction_manager)
      @money = money
      @price = price
      @transaction_manager = transaction_manager
    end

    def determine_and_issue
      issue_change(determine_change)
    end

    private

    attr_reader :transaction_manager, :money, :price

    def determine_change
      return unless money > price

      difference = money - price
      change = {}
      change = select_change_from_available_coins(change, difference)

      display.insufficient_change(difference) if difference.positive?
      change.select { |_, v| v.positive? }
    end

    def select_change_from_available_coins(change, difference)
      available_coins.each do |coin_stock|
        denomination = coin_stock.item.value
        div = difference.divmod(denomination)
        change[denomination] = [div[0], coin_stock.quantity].min
        difference = div[1] + ((div[0] - change[denomination]) * denomination)
        break if difference.zero?
      end
      change
    end

    def issue_change(change)
      return unless change

      change.each do |denomination, number|
        correct_coin = available_coins.select { |coin_stock| coin_stock.item.value == denomination }.first
        correct_coin.release(number)
        display.issue_change(denomination, number)
      end
    end

    def computer
      transaction_manager.computer
    end

    def display
      computer.display
    end

    def products
      computer.products
    end

    def available_coins
      computer.coins.select { |coin_stock| coin_stock.quantity.positive? }
    end

    def accepted_coins
      Coin.accepted_coins
    end
  end
end
