RSpec.describe VendingMachine::ChangeManager do
  describe '.determine_and_issue' do
    subject { described_class.determine_and_issue(money: money, price: price, transaction_manager: transaction_manager) }
    let(:transaction_manager) { VendingMachine::TransactionManager.new(computer: computer) }
    let(:computer) { VendingMachine::Computer.new }

    context 'when the money is equal to price' do
      let(:money) { 1 }
      let(:price) { 0.5 }

      it { is_expected.to be_nil }
    end

    context 'when the money is greater than price' do
      let(:money) { 10 }
      let(:price) { 10 }

      it { is_expected.to be_nil }
    end
  end
end