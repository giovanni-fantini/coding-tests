RSpec.describe VendingMachine::Coin do
  describe '.accepted_coins' do
    let(:expected_result) { ["£0.01", "£0.02", "£0.05", "£0.1", "£0.2", "£0.5", "£1", "£2"] }

    it 'returns the formatted list of accepted coins' do
      expect(described_class.accepted_coins).to eq(expected_result)
    end
  end

  describe '#new' do
    subject { described_class.new(value: value) }

    context 'when the value is an accepted one' do
      let(:value) { 0.10 }

      it 'instantiates the coin and exposes value and name methods', :aggreagate_failures do
        obj = subject
        expect(obj).to be_an_instance_of(VendingMachine::Coin)
        expect(obj.name).to eq('Ten cents')
        expect(obj.value).to eq(0.10)
      end
    end

    context 'when the value is an invalid one' do
      let(:value) { 0.30 }
      let(:accepted_coins) { ["£0.01", "£0.02", "£0.05", "£0.1", "£0.2", "£0.5", "£1", "£2"] }

      it 'raises an InvalidCoinError' do
        expect{ subject }.to raise_error(VendingMachine::InvalidCoinError, "the provided coin value is not accepted. Accepted values: #{accepted_coins}")
      end
    end
  end
end