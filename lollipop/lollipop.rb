require 'rspec'
require 'pry-byebug'

class CurrencyNumberFormatter
  NUMBER_DECIMALS = 2
  CURRENCY_SYMBOL = '£'.freeze

  def initialize(string_input)
    @input = string_input
  end

  def call
    # split input into array
    decimals_array = input.chars
    # separate pre and post decimal digits
    decimal_separator_index = -1 - NUMBER_DECIMALS
    digits_array = decimals_array.slice!(0..decimal_separator_index)
    # insert decimal separator
    decimals_array.unshift('.')
    # inserting thousands separators at right indexes
    add_thousands_separators(digits_array)
    # compose final output with currency symbol and join into string
    output_array = [CURRENCY_SYMBOL] + digits_array + decimals_array
    output_array.join
  end

  private

  attr_reader :input

  def add_thousands_separators(digits_array)
    number_of_digits = digits_array.size
    # guard clause for input not requiring manipulation
    return digits_array unless number_of_digits >= 4

    position = -4
    # loop to insert separators every 3 digits starting from -3 until number of digits to work is <= 3
    while number_of_digits > 3
      digits_array.insert(position, ',')
      number_of_digits -= 3
      position -= 4
    end

    digits_array
  end
end

input = '123456'
puts CurrencyNumberFormatter.new(input).call
