RSpec.describe Commands::CalculateTotal do
    describe '.call' do
        subject { described_class.call(pricing_rules: pricing_rules, basket: basket) }
    
        context 'with the given pricing rules' do
            let(:unit_prices) { {'A' => 50, 'B' => 30, 'C' => 20} } 
            let(:discounts) do
                {
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
            end
            let(:pricing_rules) { PricingRules.new(unit_prices: unit_prices, discounts: discounts) }
            
            context 'when the basket is [C, B, A, A, C, B, C]' do
                let(:basket) { {'C' => 3, 'B' => 2, 'A' => 2} } 
    
                it { is_expected.to eq(189.0) }
            end
    
            context 'when the basket is [B, A, B, B, A]' do
                let(:basket) { {'B' => 3, 'A' => 2} } 
    
                it { is_expected.to eq(165.0) }
            end
        end
    
        context 'when the pricing rules are changed' do
            let(:unit_prices) { {'A' => 40, 'B' => 40, 'C' => 40} } 
            let(:discounts) do
                {
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
            end
            let(:pricing_rules) { PricingRules.new(unit_prices: unit_prices, discounts: discounts) }
            
            context 'when the basket is [C, B, A, A, C, B, C]' do
                let(:basket) { {'C' => 3, 'B' => 2, 'A' => 2} } 
    
                it { is_expected.to eq(176.0) }
            end
    
            context 'when the basket is [B, A, B, B, A]' do
                let(:basket) { {'B' => 3, 'A' => 2} } 
    
                it { is_expected.to eq(135.0) }
            end
        end
    end
end