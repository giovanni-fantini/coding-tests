# frozen_string_literal: true

describe ToyRobot do
  let(:toy_robot) { ToyRobot.new(id: 1, position: [1, 2], direction: 'NORTH') }

  describe '#initialize' do
    it 'should set position and direction as attributes' do
      expect(toy_robot.position.current).to eq([1, 2])
      expect(toy_robot.direction.current).to eq('NORTH')
    end
  end

  describe '#turn_left' do
    it 'should change the toy_robot\'s direction to the left' do
      expect { toy_robot.turn_left }.to change { toy_robot.direction.current }
        .to('WEST')
    end
  end

  describe '#turn_right' do
    it 'should change the toy_robot\'s direction to the right' do
      expect { toy_robot.turn_right }.to change { toy_robot.direction.current }
        .to('EAST')
    end
  end

  describe '#calculate_new_position' do
    it 'should calculate and store the expected new position' do
      expect(toy_robot.calculate_new_position).to eq([1, 3])
    end
  end

  describe '#move' do
    it 'should change the current position coordinates accordingly' do
      toy_robot.calculate_new_position
      expect { toy_robot.move }.to change { toy_robot.position.current }
        .to([1, 3])
    end
  end
end
