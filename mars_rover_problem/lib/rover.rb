class Rover
    attr_reader :id, :position, :direction, :alive
    
    def initialize(args)
        @id = args[:id]
        @position = Position.new(args[:position])
        @direction = Direction.new(args[:direction])
        @alive = true
        @calculated_position = []
    end
    
    def turn_left
        @direction.current = @direction.left
    end
    
    def turn_right
        @direction.current = @direction.right
    end
    
    def calculate_new_position
        case @direction.current
        when "N"
            @calculated_position = @position.to_north
        when "E"
            @calculated_position = @position.to_east
        when "S"
            @calculated_position = @position.to_south
        when "W"
            @calculated_position = @position.to_west
        end
    end
    
    def move
        @position.current = @calculated_position
    end

    def kill
        @alive = false
    end
end