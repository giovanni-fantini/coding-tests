# frozen_string_literal: true

class Direction
  attr_accessor :current

  DIRECTIONS = %w[NORTH EAST SOUTH WEST].freeze

  def initialize(direction)
    @current = direction
  end

  def left
    DIRECTIONS[DIRECTIONS.index(current) - 1]
  end

  def right
    DIRECTIONS[DIRECTIONS.index(current) - 3]
  end
end
