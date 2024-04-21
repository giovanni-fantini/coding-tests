# frozen_string_literal: true

module Commands
  class ParseBasket
    def self.call(input:)
      new(input).call
    end

    def initialize(input)
      @input = input
    end

    def call
      parse_basket(input)
    end

    private

    attr_reader :input

    def parse_basket(input)
      File.read(input).chars.select { |c| c =~ /\w/ }
    end
  end
end
