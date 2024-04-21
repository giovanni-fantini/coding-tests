# frozen_string_literal: true

class CommandError < StandardError
end

class CommandExecutor
  class << self
    def call(input:)
      raise ArgumentError, 'Invalid file path' unless File.exist?(input)

      new(input).call
    end
  end

  def initialize(input)
    @input = Parser.call(input: input)
    @table_top = TableTop.new
    @toy_robot = place_on_table_top
  end

  def call
    input[:commands].each do |command|
      execute_command(command)
    end
  end

  private

  attr_reader :input, :table_top, :toy_robot

  # rubocop:disable MethodLength
  def execute_command(command)
    case command
    when 'MOVE'
      toy_robot.move if table_top.valid_position?(
        toy_robot.calculate_new_position
      )
    when 'LEFT'
      toy_robot.turn_left
    when 'RIGHT'
      toy_robot.turn_right
    when 'REPORT'
      report_output(toy_robot)
    end
  end

  # rubocop:enable MethodLength

  def place_on_table_top
    unless table_top.valid_position?(input[:toy_robot][:position])
      raise CommandError, 'Robot placed in invalid position'
    end

    ToyRobot.new(input[:toy_robot])
  end

  # rubocop:disable Metrics/LineLength
  def report_output(toy_robot)
    print "#{toy_robot.position.current[0]},#{toy_robot.position.current[1]},#{toy_robot.direction.current}"
  end
end

# rubocop:enable Metrics/LineLength
