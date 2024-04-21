# frozen_string_literal: true

require_relative 'parser'
require_relative 'table_top'
require_relative 'direction'
require_relative 'position'
require_relative 'toy_robot'
require_relative 'command_executor'

CommandExecutor.call(input: ARGV.first.to_s)
