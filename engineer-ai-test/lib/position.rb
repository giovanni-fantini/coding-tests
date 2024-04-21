# frozen_string_literal: true

class Position
  attr_accessor :current

  def initialize(position)
    @current = position
  end

  def to_north
    [current[0], current[1] + 1]
  end

  def to_south
    [current[0], current[1] - 1]
  end

  def to_east
    [current[0] + 1, current[1]]
  end

  def to_west
    [current[0] - 1, current[1]]
  end
end
