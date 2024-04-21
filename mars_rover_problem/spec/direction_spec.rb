describe Direction do
    let(:direction) { Direction.new("N") }
    
    describe '#initialize' do
        it 'should set current direction as attribute and expose a reader for it' do
            expect(direction.current).to eq("N")
        end
    end

    describe '#left' do 
        it 'should return the direction to the left of the current' do
            expect(direction.left).to eq("W")
            expect(Direction.new("S").left).to eq("E")
            expect(Direction.new("E").left).to eq("N")
            expect(Direction.new("W").left).to eq("S")
        end
    end

    describe '#right' do 
        it 'should return the direction to the right of the current' do
            expect(direction.right).to eq("E")
            expect(Direction.new("W").right).to eq("N")
            expect(Direction.new("S").right).to eq("W")
            expect(Direction.new("E").right).to eq("S")
        end
    end
end
