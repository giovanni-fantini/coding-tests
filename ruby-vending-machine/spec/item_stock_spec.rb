RSpec.describe VendingMachine::ItemStock do
  describe '#new' do
    subject { described_class.new(item: item, quantity: quantity) }
    let(:item) { VendingMachine::Product.new(name: 'apple', price: 0.50) }

    context 'when the quantity is a valid non-zero integer' do
      let(:quantity) { 5 }

      it 'instantiates the product and exposes price and name methods', :aggreagate_failures do
        obj = subject
        expect(obj).to be_an_instance_of(VendingMachine::ItemStock)
        expect(obj.item).to eq(item)
        expect(obj.quantity).to eq(5)
      end
    end

    context 'when the quantity is not a valid integer' do
      let(:quantity) { 'something' }

      it 'raises an InvalidItemStockError' do
        expect{ subject }.to raise_error(VendingMachine::InvalidItemStockError, "the provided quantity for item #{item.name} is not a valid non-zero integer")
      end
    end
  end

  describe '#release' do
    subject {item_stock.release }
    let(:item_stock) { VendingMachine::ItemStock.new(item: item, quantity: quantity) }
    let(:item) { VendingMachine::Product.new(name: 'apple', price: 0.50) }

    context 'when the remaining quantity is more than zero' do
      let(:quantity) { 10 }

      it 'decreases the remaining quantity by 1' do
        expect { subject }.to change(item_stock, :quantity).by(-1)
      end
    end

    context 'when the quantity is zero' do
      let(:quantity) { 0 }

      it 'raises an EmptyStockError' do
        expect{ subject }.to raise_error(VendingMachine::InvalidItemStockError, "the provided quantity for item #{item.name} is not a valid non-zero integer")
      end
    end
  end

  describe '#restock' do
    subject {item_stock.restock(restock_q) }
    let(:item_stock) { VendingMachine::ItemStock.new(item: item, quantity: quantity) }
    let(:item) { VendingMachine::Product.new(name: 'apple', price: 0.50) }
    let(:quantity) { 10 }
    let(:restock_q) { 5 }

    it 'increases the remaining quantity by the required number' do
      expect { subject }.to change(item_stock, :quantity).by(5)
    end
  end
end