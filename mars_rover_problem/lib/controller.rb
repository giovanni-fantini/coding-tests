require "pry-byebug"

class Controller
    def initialize(input)
        raise ArgumentError.new("Invalid file path") if !File.exist?(input)
        @input = Parser.new(input).parse_text
        @plateau = Plateau.new(@input[:upper_bounds])
    end
    
    def land_on_plateau
        @input[:rovers].each do |rover_inputs|
            rover = Rover.new(rover_inputs)
            @plateau.track_rover(rover) if @plateau.valid_position?(rover.position.current)
        end
    end
    
    def execute_commands
        @input[:commands].each do |command|
            rover = @plateau.find_rover(command[:id])
            command[:orders].each do |order|
                case order
                when "M"
                    if @plateau.valid_position?(rover.calculate_new_position)
                        rover.move 
                    elsif @plateau.beacon?(rover.position.current)
                        
                    else
                        rover.kill
                    end
                when "L"
                    rover.turn_left
                when "R"
                    rover.turn_right
                end
            end
        end
    end
    
    def report_output
        @plateau.rovers.each do |rover|
            if rover.alive == false
                puts "#{rover.position.current[0]} #{rover.position.current[1]} #{rover.direction.current} RIP"
            else
                puts "#{rover.position.current[0]} #{rover.position.current[1]} #{rover.direction.current}"
            end
        end
    end
end