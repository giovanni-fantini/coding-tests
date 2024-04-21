describe Rover do 
    let(:rover) { Rover.new({id: 1, position: [1,2], direction: "N"}) }

    describe '#initialize' do
        it 'should set id, position and direction as attributes and expose readers for them' do
            expect(rover.id).to eq(1)
            expect(rover.position.current).to eq([1,2])
            expect(rover.direction.current).to eq("N")
        end
        
        it 'should create a calculated position placeholder' do
            expect(rover.instance_variable_get(:@calculated_position)).to eq([])
        end
    end
    
    context 'when rover is facing North and at position [1,2]' do
        describe '#turn_left' do 
            it 'should change the rover\'s direction to the left' do
                expect{ rover.turn_left }.to change{ rover.direction.current}.to("W")
            end
        end
        
        describe '#turn_right' do 
            it 'should change the rover\'s direction to the right' do
                expect{ rover.turn_right }.to change{ rover.direction.current}.to("E")
            end
        end
        
        describe '#calculate_new_position' do
            it 'should calculate and store the expected new position in a variable' do
                expect{ rover.calculate_new_position }
                .to change{ rover.instance_variable_get(:@calculated_position)}.to([1,3])
            end
        end

        describe '#move' do
            it 'should change the current position coordinates accordingly' do
                rover.calculate_new_position
                expect{ rover.move }.to change{ rover.position.current}.to([1,3])
            end
        end
    end
    
    context 'when rover is facing South and at position [1,5]' do
        let(:rover) { Rover.new({id: 1, position: [1,5], direction: "S"}) }
        describe '#turn_left' do 
            it 'should change the rover\'s direction to the left' do
                expect{ rover.turn_left }.to change{ rover.direction.current}.to("E")
            end
        end
        
        describe '#turn_right' do 
            it 'should change the rover\'s direction to the right' do
                expect{ rover.turn_right }.to change{ rover.direction.current}.to("W")
            end
        end
        
        describe '#move' do
            it 'should change the current position coordinates accordingly' do
                rover.calculate_new_position
                expect{ rover.move }.to change{ rover.position.current}.to([1,4])
            end
        end
        
        describe '#calculate_new_position' do
            it 'should calculate and store the expected new position in a variable' do
                expect{ rover.calculate_new_position }
                .to change{ rover.instance_variable_get(:@calculated_position)}.to([1,4])
            end
        end
    end

    context 'when rover is facing West and at position [5,1]' do
        let(:rover) { Rover.new({id: 1, position: [5,1], direction: "W"}) }
        describe '#turn_left' do 
            it 'should change the rover\'s direction to the left' do
                expect{ rover.turn_left }.to change{ rover.direction.current}.to("S")
            end
        end
        
        describe '#turn_right' do 
            it 'should change the rover\'s direction to the right' do
                expect{ rover.turn_right }.to change{ rover.direction.current}.to("N")
            end
        end
        
        describe '#move' do
            it 'should change the current position coordinates accordingly' do
                rover.calculate_new_position
                expect{ rover.move }.to change{ rover.position.current}.to([4,1])
            end
        end
        
        describe '#calculate_new_position' do
            it 'should calculate and store the expected new position in a variable' do
                expect{ rover.calculate_new_position }
                .to change{ rover.instance_variable_get(:@calculated_position)}.to([4,1])
            end
        end
    end

    context 'when rover is facing East and at position [4,2]' do
        let(:rover) { Rover.new({id: 1, position: [4,2], direction: "E"}) }
        describe '#turn_left' do 
            it 'should change the rover\'s direction to the left' do
                expect{ rover.turn_left }.to change{ rover.direction.current}.to("N")
            end
        end
        
        describe '#turn_right' do 
            it 'should change the rover\'s direction to the right' do
                expect{ rover.turn_right }.to change{ rover.direction.current}.to("S")
            end
        end
        
        describe '#move' do
            it 'should change the current position coordinates accordingly' do
                rover.calculate_new_position
                expect{ rover.move }.to change{ rover.position.current}.to([5,2])
            end
        end
        
        describe '#calculate_new_position' do
            it 'should calculate and store the expected new position in a variable' do
                expect{ rover.calculate_new_position }
                .to change{ rover.instance_variable_get(:@calculated_position)}.to([5,2])
            end
        end
    end
end

# describe '#move' do 
#     context 'when rover is on Northern border of plateau' do
#         it 'should not move if its direction is North' do
#             rover = Rover.new(1, [1,5], "N", plateau) 
#             expect{ rover.move }.not_to change{ rover.position}
#         end

#         it 'should move if facing another direction (e.g. South)' do
#             rover = Rover.new(1, [1,5], "S", plateau)
#             expect{ rover.move }.to change{ rover.position}.to([1,4])
#         end
#     end

#     context 'when rover is on Eastern border of plateau' do
#         it 'should not move if its direction is East' do
#             rover = Rover.new(1, [5,1], "E", plateau) 
#             expect{ rover.move }.not_to change{ rover.position}
#         end

#         it 'should move if facing another direction (e.g. North)' do
#             rover = Rover.new(1, [5,1], "N", plateau)
#             expect{ rover.move }.to change{ rover.position}.to([5,2])
#         end
#     end

#     context 'when rover is on Southern border of plateau' do
#         it 'should not move if its direction is South' do
#             rover = Rover.new(1, [1,0], "S", plateau) 
#             expect{ rover.move }.not_to change{ rover.position}
#         end

#         it 'should move if facing another direction (e.g. West)' do
#             rover = Rover.new(1, [1,0], "W", plateau)
#             expect{ rover.move }.to change{ rover.position}.to([0,0])
#         end
#     end

#     context 'when rover is on Western border of plateau' do
#         it 'should not move if its direction is West' do
#             rover = Rover.new(1, [0,1], "W", plateau) 
#             expect{ rover.move }.not_to change{ rover.position}
#         end

#         it 'should move if facing another direction (e.g. East)' do
#             rover = Rover.new(1, [0,1], "E", plateau)
#             expect{ rover.move }.to change{ rover.position}.to([1,1])
#         end
#     end

#     context 'when rover not on plateau boundaries' do 
#         it 'should move when facing North' do
#             expect{ rover.move }.to change{ rover.position}.to([1,3])
#         end

#         it 'should move when facing South' do
#             rover.direction.current = "S"
#             expect{ rover.move }.to change{ rover.position}.to([1,1])
#         end

#         it 'should move when facing East' do
#             rover.direction.current = "E"
#             expect{ rover.move }.to change{ rover.position}.to([2,2])
#         end

#         it 'should move when facing West' do
#             rover.direction.current = "W"
#             expect{ rover.move }.to change{ rover.position}.to([0,2])
#         end
#     end

#     context 'when rover is facing another rover' do
#         it 'should not move' do
#             plateau.(2, [1,3])
#             expect{ rover.move }.not_to change{ rover.position}
#         end
#     end
# end