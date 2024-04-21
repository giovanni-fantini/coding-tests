require_relative "parser"
require_relative "plateau"
require_relative "direction"
require_relative "position"
require_relative "rover"
require_relative "controller"

controller = Controller.new(ARGV.first.to_s)
controller.land_on_plateau
controller.execute_commands
controller.report_output