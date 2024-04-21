RSpec.describe Commands::ParseUnitPrices do
    describe '.call' do
        subject { described_class.call(input: input) }

        context 'with the given discount file' do
            let(:input) { 'data/unit_prices.csv' }
    
            expected_result = {'A' => 50, 'B' => 30, 'C' => 20}
    
            it { is_expected.to eq(expected_result) }
        end
    
        context 'with a different discounts file' do
            let(:input) { 'spec/data/unit_prices.csv' }
    
            expected_result = {'A' => 40, 'B' => 40, 'C' => 40}
    
            it { is_expected.to eq(expected_result) }
        end
    end  
end
