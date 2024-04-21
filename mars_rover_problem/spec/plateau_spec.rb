require "pry-byebug"
describe Plateau do
    let(:plateau) { Plateau.new([5,5]) }
    let(:rover) { Rover.new({id: 1, position: [1,2], direction: "N"}) }
    
    it 'should set a reader for the attribute rovers' do
        expect(plateau.rovers).to eq([])
    end
    
    describe '#initialize' do
        it 'should store its X and Y axes dimensions' do
            expect(plateau.instance_variable_get(:@x_axis)).to eq([0,5])
            expect(plateau.instance_variable_get(:@y_axis)).to eq([0,5])
        end
    end
 
    describe '#valid_position?' do
        context 'when the coordinates are occupied by another rover' do
            it 'should return false' do
                plateau.instance_variable_set(:@rovers, [rover])
                expect(plateau.valid_position?([1,2])).to eq(false)
            end
        end
        
        context 'when the coordinates are outside of the plateau boundaries' do
            it 'should return false' do 
                expect(plateau.valid_position?([1,6])).to eq(false)
                expect(plateau.valid_position?([6,1])).to eq(false)
                expect(plateau.valid_position?([6,6])).to eq(false)
                expect(plateau.valid_position?([-1,3])).to eq(false)
                expect(plateau.valid_position?([3,-1])).to eq(false)
                expect(plateau.valid_position?([-1,-1])).to eq(false)
            end
        end
        
        context 'when the coordinates are inside of the plateau boundaries' do
            it 'should return true' do 
                expect(plateau.valid_position?([1,3])).to eq(true)
                expect(plateau.valid_position?([3,1])).to eq(true)
                expect(plateau.valid_position?([0,5])).to eq(true)
                expect(plateau.valid_position?([5,0])).to eq(true)
                expect(plateau.valid_position?([0,0])).to eq(true)
                expect(plateau.valid_position?([5,5])).to eq(true)
            end
        end
    end
    
    describe '#track_rover' do
        it 'should store the rover info in an array' do
            plateau.track_rover(rover)
            expect(plateau.rovers.first).to be_kind_of(Rover)
            expect(plateau.rovers.first.id).to eq(1)
            expect(plateau.rovers.first.position.current).to eq([1,2])
            expect(plateau.rovers.first.direction.current).to eq("N")
        end
    end

    describe '#find_rover' do
        it 'should retrieve the right rover based on the supplied id' do
            rover2 = Rover.new({id: 2, position: [1,3], direction: "S"})
            plateau.track_rover(rover)
            plateau.track_rover(rover2)
            expect(plateau.find_rover(1)).to be_kind_of(Rover)
            expect(plateau.find_rover(1).position.current).to eq([1,2])
            expect(plateau.find_rover(1).direction.current).to eq("N") 
        end
    end
end