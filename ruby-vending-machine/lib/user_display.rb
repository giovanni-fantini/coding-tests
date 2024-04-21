# frozen_string_literal: true

module VendingMachine
  class InvalidSelectionError < StandardError; end

  class UserDisplay
    LIST_OPTIONS = %i[actions products coins].freeze

    def initialize(input: $stdin, output: $stdout)
      @input = input
      @output = output
    end

    def list(objects, type)
      raise InvalidSelectionError unless LIST_OPTIONS.include?(type)

      counter = 1

      puts "List of available #{type}:"
      objects.each do |object|
        puts "(#{counter}) #{build_message(object, type)}"
        counter += 1
      end
    end

    def get_list_input(objects)
      puts 'Please type the number in the parenthesis for the desired choice'
      selection = ask_input.to_i
      raise InvalidSelectionError unless (1..objects.length).include?(selection)

      objects[selection - 1]
    end

    def ask_product_info
      puts 'Please type product name'
      name = ask_input
      puts 'Please type product price'
      price = ask_input.to_f
      puts 'Please provide quantity of product in integer numbers'
      quantity = ask_input.to_i
      puts 'Do you want to add more Y/N?'
      continue = ask_input
      { name: name, price: price, quantity: quantity, continue: continue }
    end

    def ask_coin_info(accepted_coins)
      puts "Please type coin value as decimal (e.g. 5p is 0.05). Accepted coins: #{accepted_coins}"
      value = ask_input.to_f
      puts 'Please provide quantity of coin in integer numbers'
      quantity = ask_input.to_i
      puts 'Do you want to add more Y/N?'
      continue = ask_input
      { value: value, quantity: quantity, continue: continue }
    end

    def output_error(error)
      puts "Sorry, #{error}, please try again."
    end

    def clear_screen
      print `clear`
    end

    def invalid_selection
      message = 'your selection was invalid'
      display_error(message)
    end

    def pause
      puts 'Press enter to return to the list of actions'
      ask_input
    end

    def ask_money(price, accepted_coins)
      puts "Please insert £#{price.round(1)}. The accepted coins are: #{accepted_coins}"
      puts 'Please type amount in £ or type C to cancel transaction'
      ask_input
    end

    def insufficient_funds
      puts 'Sorry, the amount of money inserted was insufficient'
    end

    def insufficient_change(amount)
      puts "Sorry, there is not sufficient change. Amount missing: £#{amount.round(1)}"
    end

    def issue_change(denomination, number)
      puts "Please take #{number}x£#{denomination} coins"
    end

    def issue_product(product)
      puts "Please take #{product}. Thank you."
    end

    def restock_existing?(type)
      puts "Would you like to restock one of the existing #{type} or add a new one?"
      puts 'Type Y for existing'
      return true if ask_input == 'Y'
    end

    def ask_restock_quantity(item)
      puts "Please type restocking quantity for #{item}"
      ask_input.to_i
    end

    private

    def ask_input
      gets.chomp
    end

    def build_message(object, type)
      case type
      when :actions
        object
      when :products
        "#{object.item.name} | price: #{object.item.price} | available quantity: #{object.quantity}"
      when :coins
        "#{object.item.name} | value: #{object.item.value} | available quantity: #{object.quantity}"
      end
    end
  end
end
