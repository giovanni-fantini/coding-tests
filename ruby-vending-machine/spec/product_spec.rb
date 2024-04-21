RSpec.describe VendingMachine::Product do
  describe '#new' do
    subject { described_class.new(name: name, price: price) }
    let(:name) { 'apple' }

    context 'when the price is a valid non-zero decimal' do
      let(:price) { 0.50 }

      it 'instantiates the product and exposes price and name methods', :aggreagate_failures do
        obj = subject
        expect(obj).to be_an_instance_of(VendingMachine::Product)
        expect(obj.name).to eq('apple')
        expect(obj.price).to eq(0.50)
      end
    end

    context 'when the price is not a valid decimal' do
      let(:price) { 'something' }

      it 'raises an InvalidProductError' do
        expect{ subject }.to raise_error(VendingMachine::InvalidProductError, "the provided price for product #{name} is not a valid non-zero decimal")
      end
    end
  end
end