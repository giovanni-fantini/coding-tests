RSpec.describe Commands::ParseBasket do
    describe '.call' do
        subject { described_class.call(input: input) }

        context 'with the given basket file' do
            let(:input) { 'data/basket.txt' }
    
            it { is_expected.to eq(['C', 'B', 'A', 'A', 'C', 'B', 'C']) }
        end
    
        context 'when the basket file contains an unformatted string of letters' do
            let(:input) { 'spec/data/basket.txt' }
    
            it { is_expected.to eq(['B', 'A', 'B', 'B', 'A']) }
        end
    end 
end
