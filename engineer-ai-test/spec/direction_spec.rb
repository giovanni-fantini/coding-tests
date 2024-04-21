# frozen_string_literal: true

describe Direction do
  let(:direction) { Direction.new('NORTH') }

  describe '#initialize' do
    it 'should set current direction as attribute and expose a reader for it' do
      expect(direction.current).to eq('NORTH')
    end
  end

  describe '#left' do
    it 'should return the direction to the left of the current' do
      expect(direction.left).to eq('WEST')
      expect(Direction.new('SOUTH').left).to eq('EAST')
      expect(Direction.new('EAST').left).to eq('NORTH')
      expect(Direction.new('WEST').left).to eq('SOUTH')
    end
  end

  describe '#right' do
    it 'should return the direction to the right of the current' do
      expect(direction.right).to eq('EAST')
      expect(Direction.new('WEST').right).to eq('NORTH')
      expect(Direction.new('SOUTH').right).to eq('WEST')
      expect(Direction.new('EAST').right).to eq('SOUTH')
    end
  end
end
