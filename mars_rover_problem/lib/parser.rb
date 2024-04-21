class Parser
    def initialize(input)
        @input = input
        @output = { upper_bounds: [], rovers: [], commands: []}
        @next_id = 1
    end
    
    def parse_text
        next_line = 1
        File.readlines(@input).each do |line|
            if next_line == 1
                parse_upper_bounds(line)
            elsif next_line.even?
                parse_rovers(line)
            else
                parse_rover_cmds(line)
                @next_id += 1
            end
            next_line += 1
        end
        @output
    end
    
    private
    
    def parse_upper_bounds(line)
        @output[:upper_bounds] = line.split(" ").map {|num| num.to_i }
    end
    
    def parse_rovers(line)
        info = line.split(" ")
        @output[:rovers] << {
            id: @next_id,
            position: [info[0].to_i, info[1].to_i ],
            direction: info[2]
        }
    end
    
    def parse_rover_cmds(line)
        @output[:commands] << {id: @next_id, orders: line.strip.chars}
    end
end