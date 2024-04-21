# frozen_string_literal: true

class ToyRobot
  attr_reader :position, :direction

  def initialize(robot_inputs)
    @position = Position.new(robot_inputs[:position])
    @direction = Direction.new(robot_inputs[:direction])
    @calculated_position = []
  end

  def turn_left
    direction.current = direction.left
  end

  def turn_right
    direction.current = direction.right
  end

  def calculate_new_position
    case direction.current
    when 'NORTH'
      @calculated_position = position.to_north
    when 'EAST'
      @calculated_position = position.to_east
    when 'SOUTH'
      @calculated_position = position.to_south
    when 'WEST'
      @calculated_position = position.to_west
    end
  end

  def move
    position.current = @calculated_position
  end
end
