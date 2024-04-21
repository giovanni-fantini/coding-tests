require_relative 'test.rb'

RSpec.describe ReceiptGenerator do
  describe 'call' do
    it 'outputs the subtotals hash and the total for the cart' do
      input = { 'milk_bottle' => 1, 'salad' => 1 }
      
      expect(STDOUT).to receive(:puts).with([{"milk_bottle"=>{:quantity=>1, :subtotal=>2}}, {"salad"=>{:quantity=>1, :subtotal=>1}}])
      expect(STDOUT).to receive(:puts).with('Total: 3.0')
      described_class.new(input).call
    end
  end
end