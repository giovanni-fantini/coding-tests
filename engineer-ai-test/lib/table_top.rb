# frozen_string_literal: true

class TableTop
  def initialize
    @x_axis = [0, 5]
    @y_axis = [0, 5]
  end

  def valid_position?(position)
    return false unless position[0].between?(@x_axis[0], @x_axis[1])

    position[1].between?(@y_axis[0], @y_axis[1])
  end
end
