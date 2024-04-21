# frozen_string_literal: true

module VendingMachine
  class InvalidCoinError < StandardError; end
  class Coin
    ACCEPTED_COINS = {
      'One pence' => 0.01,
      'Two pence' => 0.02,
      'Five pence' => 0.05,
      'Ten cents' => 0.1,
      'Twenty cents' => 0.2,
      'Fifty cents' => 0.5,
      'One pound' => 1,
      'Two pounts' => 2
    }.freeze

    attr_reader :name, :value

    def self.accepted_coins
      @accepted_coins ||= ACCEPTED_COINS.map { |_k, v| "£#{v}" }
    end

    def initialize(value:)
      @value = value
      @name = set_name
    end

    private

    def set_name
      ACCEPTED_COINS.each do |k, v|
        return k if value == v
      end

      raise VendingMachine::InvalidCoinError,
            "the provided coin value is not accepted. Accepted values: #{self.class.accepted_coins}"
    end
  end
end
