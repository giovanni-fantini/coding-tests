# frozen_string_literal: true

class Parser
  class << self
    def call(input:)
      new(input).call
    end
  end

  def initialize(input)
    @input = input
    @output = {}
  end

  def call
    File.readlines(input).each do |line|
      @cmds = line.split(' ')
      @place_i = cmds.index('PLACE')
      raise CommandError, 'No place command found' unless place_i

      parse_toy_robot_position
      parse_commands
    end
    @output
  end

  private

  attr_reader :cmds, :place_i, :input
  attr_accessor :output

  def parse_toy_robot_position
    position_cmds = cmds[place_i + 1].split(',')
    output[:toy_robot] = {
      position: [position_cmds[0].to_i, position_cmds[1].to_i],
      direction: position_cmds[2]
    }
  end

  def parse_commands
    output[:commands] = cmds.slice((place_i + 2)..-1)
  end
end
