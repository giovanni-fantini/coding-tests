# frozen_string_literal: true

describe Position do
  let(:position) { Position.new([1, 2]) }

  describe '#initialize' do
    it 'should set current position as attribute and expose a reader for it' do
      expect(position.current).to eq([1, 2])
    end
  end

  describe '#to_north' do
    it 'should return coordinates increased by 1 on the Y axis' do
      expect(position.to_north).to eq([1, 3])
    end
  end

  describe '#to_south' do
    it 'should return coordinates decreased by 1 on the Y axis' do
      expect(position.to_south).to eq([1, 1])
    end
  end

  describe '#to_east' do
    it 'should return coordinates increased by 1 on the X axis' do
      expect(position.to_east).to eq([2, 2])
    end
  end

  describe '#to_west' do
    it 'should return coordinates decreased by 1 on the X axis' do
      expect(position.to_west).to eq([0, 2])
    end
  end
end
