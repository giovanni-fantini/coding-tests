require 'rails_helper'

RSpec.describe Project, type: :model do
  describe 'validations' do
    it { should validate_inclusion_of(:status).in_array(['not_started', 'in_progress', 'done']) }
    it { should validate_presence_of(:status) }
  end

  describe '#interaction_history' do
    subject { project.interaction_history }
    let(:project) { described_class.new(name: 'Test project', status: 'not_started') }
    let(:first_comment) { instance_double(Comment, project: project, body: 'First comment', created_at: "2023-03-05 21:25:50.038566") }
    let(:first_status_change) { instance_double(StatusChange, project: project, from: 'not_started', to: 'in_progress', created_at: "2023-03-05 21:30:50.038566") }
    let(:second_comment) { instance_double(Comment, project: project, body: 'Second comment', created_at: "2023-03-05 21:35:50.038566") }
    let(:second_status_change) { instance_double(StatusChange, project: project, from: 'in_progress', to: 'done', created_at: "2023-03-05 21:40:50.038566") }
    let(:expected_interaction_history) { [second_status_change, second_comment, first_status_change, first_comment] }

    before do 
      allow(project).to receive(:comments).and_return([first_comment, second_comment])
      allow(project).to receive(:status_changes).and_return([first_status_change, second_status_change])
    end

    it 'returns comments and status changes for the project in desc order of time' do
      expect(subject).to eq(expected_interaction_history)
    end
  end
end
