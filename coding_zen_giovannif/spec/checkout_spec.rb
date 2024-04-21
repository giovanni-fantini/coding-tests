RSpec.describe Checkout do
    subject { described_class.new(pricing_rules: pricing_rules) }
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
    
    describe '#scan' do
        it 'should add the object to the basket' do
            expect { subject.scan('A') }.to change{subject.basket}.from({}).to({'A' => 1})
        end
    end

    describe '#scan_multiple' do
        it 'should add all the items to the basket' do
            expect { subject.scan_multiple(['A','B','A']) }.to change{subject.basket}.from({}).to({'A' => 2, 'B' => 1})
        end
    end

    describe '#total' do
        it 'should call the CalculateTotal command' do
            expect(Commands::CalculateTotal).to receive(:call)
            subject.total
        end
    end
end