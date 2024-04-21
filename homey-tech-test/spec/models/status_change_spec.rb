require 'rails_helper'

RSpec.describe StatusChange, type: :model do
  describe 'validations' do
    it { should validate_presence_of(:from) }
    it { should validate_inclusion_of(:from).in_array(['not_started', 'in_progress', 'done']) }
    it { should validate_presence_of(:to) }
    it { should validate_inclusion_of(:to).in_array(['not_started', 'in_progress', 'done']) }
  end
end
