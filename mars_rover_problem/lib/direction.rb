class Direction 
    attr_accessor :current

    DIRECTIONS = ["N", "E", "S", "W"]

    def initialize(direction)
         @current = direction
    end

    def left
        DIRECTIONS[DIRECTIONS.index(@current) - 1]
    end

    def right
        DIRECTIONS[DIRECTIONS.index(@current) - 3]
    end
end