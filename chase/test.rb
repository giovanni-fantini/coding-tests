require 'httparty'
require 'json'
require 'pry-byebug'
require 'csv'

class ReceiptGenerator
  PRICES = {
    'milk_bottle' => 2.0,
    'salad' => 1.0
  }.freeze
  
  def initialize(shopping_cart_hash)
    @shopping_cart = shopping_cart_hash
  end
  
  # {milk_bottle: 1, etc}
  def call
    output_receipt
  end

  private

  attr_reader :shopping_cart

  # {milk_bottle => { quantity: 1, price: 2 }}
  def generate_shopping_cart_hash
    shopping_cart.map { |item, quantity| {item => { quantity: quantity, subtotal: quantity * PRICES[item] } } }
  end

  def calculate_total
    running_total = 0

    shopping_cart.each do |item, number| 
      running_total += (number * PRICES[item])
    end

    running_total
  end

  # {  }
  # Total:
  def output_receipt
    puts generate_shopping_cart_hash
    puts "Total: #{calculate_total}"
  end
end

class ShoppingCart
  # milk_bottle => { quantity: 1}}
  def initialize(hash_of_product_info)
    @shopping_cart = hash_of_product_info
  end

  def add
    
  end
end
