# frozen_string_literal: true

describe Parser do
  describe '.call' do
    context 'when the commands are correctly provided' do
      let(:output) { Parser.call(input: 'spec/data/test_data.txt') }

      it 'should parse the toy_robot\'s info and add them to output' do
        expect(output[:toy_robot]).to eq(
          position: [1, 2], direction: 'EAST'
        )
      end

      it 'should parse commands and add them to output' do
        expect(output[:commands]).to eq(
          %w[MOVE MOVE LEFT MOVE REPORT]
        )
      end
    end

    context 'when no place command is provided' do
      it 'should raise an exception' do
        expect { Parser.call(input: 'spec/data/no_place_command.txt') }
          .to raise_error(
            CommandError, 'No place command found'
          )
      end
    end
  end
end
