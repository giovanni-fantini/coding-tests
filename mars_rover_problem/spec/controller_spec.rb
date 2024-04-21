describe Controller do
    let(:controller) {Controller.new("sample_data.txt")}
    let(:plateau) { controller.instance_variable_get(:@plateau) }
    
    describe '#initialize' do
        it 'shouldn\'t take  an unexisting file as input' do
            expect{Controller.new("unexisting_file.txt")}.to raise_error(ArgumentError)
        end
        
        it 'should store the parsed input as a hash' do
            expect(controller.instance_variable_get(:@input)).to be_kind_of(Hash)
        end
        
        it 'should create and store a Plateau of the specified size' do
            expect(plateau).to be_kind_of(Plateau)
            expect(plateau.instance_variable_get(:@x_axis)).to eq([0,5])
            expect(plateau.instance_variable_get(:@y_axis)).to eq([0,5])
        end
    end
    
    describe '#land_on_plateau' do
        context 'when a rover\'s input position is valid' do
            it 'should store the rover instance in the Plateau' do
                controller.land_on_plateau
                first_rover = plateau.rovers.first
                expect(first_rover).to be_kind_of(Rover)
                expect(first_rover.id).to eq(1)
                expect(first_rover.position.current).to eq([1,2])
                expect(first_rover.direction.current).to eq("N")
            end
        end
        
        context 'when a rover\'s input position is invalid' do
            it 'should not store the rover instance in the Plateau' do
                rover = {id:1, position: [1,2], direction: "N"}
                rover2 = {id:2, position: [1,2], direction: "E"}
                rover3 = {id: 3, position: [6,6], direction: "S"}
                controller.instance_variable_set(:@input, {rovers: [rover, rover2, rover3]})
                controller.land_on_plateau
                last_rover = plateau.rovers.first
                expect(last_rover).to be_kind_of(Rover)
                expect(last_rover.id).to eq(1)
                expect(last_rover.position.current).to eq([1,2])
                expect(last_rover.direction.current).to eq("N")
            end
        end
    end
    
    describe '#execute_commands' do
        it 'should send the right commands to the right rover' do
            controller.land_on_plateau
            controller.execute_commands
            expect(plateau.find_rover(2).position.current).to eq([5,1])
            expect(plateau.find_rover(2).direction.current).to eq("E")
        end
        
        context 'when the rover would move into an invalid position' do
            it 'should not send the move command' do
                rover = {id:1, position: [5,5], direction: "N"}
                command = {id: 1, orders: ["M"]}
                controller.instance_variable_set(:@input, {rovers: [rover], commands: [command]})
                controller.land_on_plateau
                controller.execute_commands
                expect(plateau.find_rover(1).position.current).to eq([5,5])
                expect(plateau.find_rover(1).direction.current).to eq("N")
            end
        end
    end
    
    describe '#report_output' do
        it 'should report the rovers\' info to the user in the right format' do  
            controller.land_on_plateau
            controller.execute_commands
            expect { controller.report_output }.to output("1 3 N\n5 1 E\n").to_stdout
        end
    end
end