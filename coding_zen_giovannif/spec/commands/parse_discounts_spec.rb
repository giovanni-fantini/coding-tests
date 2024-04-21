RSpec.describe Commands::ParseDiscounts do
    describe '.call' do
        subject { described_class.call(input: input) }

        context 'with the given discount file' do
            let(:input) { 'data/discounts.txt' }
    
            expected_result = {
                bundle_price: [
                    {
                        item_quantity: 2,
                        item_type: 'A',
                        bundle_price: 90
                    },
                    {
                        item_quantity: 3,
                        item_type: 'B',
                        bundle_price: 75
                    }
                ],
                percent_off_basket: {
                    200 => 10
                }
            }
    
            it { is_expected.to eq(expected_result) }
        end
    
        context 'with a different discounts file' do
            let(:input) { 'spec/data/discounts.txt' }
    
            expected_result = {
                bundle_price: [
                    {
                        item_quantity: 2,
                        item_type: 'A',
                        bundle_price: 60
                    },
                    {
                        item_quantity: 3,
                        item_type: 'B',
                        bundle_price: 75
                    },
                    {
                        item_quantity: 3,
                        item_type: 'C',
                        bundle_price: 80
                    }
                ],
                percent_off_basket: {
                    150 => 10,
                    200 => 20
                }
            }
    
            it { is_expected.to eq(expected_result) }
        end
    end 
end
    