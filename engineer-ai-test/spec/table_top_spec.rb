# frozen_string_literal: true

describe TableTop do
  let(:table_top) { TableTop.new }

  describe '#initialize' do
    it 'should store its X and Y axes dimensions' do
      expect(table_top.instance_variable_get(:@x_axis)).to eq([0, 5])
      expect(table_top.instance_variable_get(:@y_axis)).to eq([0, 5])
    end
  end

  describe '#valid_position?' do
    context 'when the coordinates are outside of the table_top boundaries' do
      it 'should return false' do
        expect(table_top.valid_position?([1, 6])).to eq(false)
        expect(table_top.valid_position?([6, 1])).to eq(false)
        expect(table_top.valid_position?([-1, 3])).to eq(false)
        expect(table_top.valid_position?([3, -1])).to eq(false)
      end
    end

    context 'when the coordinates are inside of the table_top boundaries' do
      it 'should return true' do
        expect(table_top.valid_position?([1, 3])).to eq(true)
        expect(table_top.valid_position?([3, 1])).to eq(true)
        expect(table_top.valid_position?([0, 5])).to eq(true)
        expect(table_top.valid_position?([5, 0])).to eq(true)
        expect(table_top.valid_position?([0, 0])).to eq(true)
        expect(table_top.valid_position?([5, 5])).to eq(true)
      end
    end
  end
end
