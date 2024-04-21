class Plateau
    attr_reader :rovers
    
    def initialize(upper_bounds)
        @x_axis = [0, upper_bounds[0]]
        @y_axis = [0, upper_bounds[1]]
        @rovers = []
    end
    
    def valid_position?(position)
        if find_by_position(position).nil?
            if position[0].between?(@x_axis[0], @x_axis[1])
                if position[1].between?(@y_axis[0], @y_axis[1])
                    return true
                end
            end
        end
        false
    end
    
    def track_rover(rover)
        @rovers << rover
    end
    
    def find_rover(id)
        @rovers.find {|rover| rover.id == id }
    end

    def beacon?(position)
        @rovers.select {|rover| rover.alive == false }.each do |rover|
            if rover.position == position
                return true
            end
        end
        false
    end
    
    private
    
    def find_by_position(position)
        @rovers.find {|rover| rover.position.current == position }
    end
end