# frozen_string_literal: true

describe CommandExecutor do
  let(:execute) { CommandExecutor.call(input: 'spec/data/test_data.txt') }

  describe '.call' do
    it 'shouldn\'t take  an unexisting file as input' do
      expect { CommandExecutor.call(input: 'unexisting_file.txt') }
        .to raise_error(ArgumentError, 'Invalid file path')
    end

    context 'when a toy_robot\'s position and commands are valid' do
      it 'should execute the commands correctly' do
        expect { execute }.to output('3,3,NORTH').to_stdout
      end
    end

    context 'when a toy_robot\'s input position is invalid' do
      let(:execute) do
        CommandExecutor.call(
          input: 'spec/data/invalid_position.txt'
        )
      end

      it 'should raise an exception' do
        expect { execute }.to raise_error(
          CommandError, 'Robot placed in invalid position'
        )
      end
    end

    context 'when the toy_robot would move into an invalid position' do
      let(:execute) do
        CommandExecutor.call(
          input: 'spec/data/move_to_invalid.txt'
        )
      end

      it 'should not execute the wrong commands' do
        expect { execute }.to output('5,5,EAST').to_stdout
      end
    end
  end
end
