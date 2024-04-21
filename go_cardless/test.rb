require 'httparty'
require 'json'
require 'pry'
require 'csv'

class ApiError < StandardError; end

class ApiClient
  def self.get_merchant_list
    response = HTTParty.get('https://simpledebit.gocardless.io/merchants')
    return response.body if response.code == 200

    raise ApiError "Api returned error with code #{response.code} and message: #{response.body.message}"
  end

  # response example:
  # {
  # "id": "M28A9",
  # "iban": "GB2756386333762976",
  # "discount": {
  #   "minimum_transaction_count": 49,
  #   "fees_discount": 7
  # },
  # "transactions": [
  #   {
  #     "amount": 54869,
  #     "fee": 290
  #   },
  #   {
  #     "amount": 50033,
  #     "fee": 297
  #   },
  def self.get_transaction_list(merchant_id)
    response = HTTParty.get("https://simpledebit.gocardless.io/merchants/#{merchant_id}")
    return response.body if response.code == 200

    raise ApiError "Api returned error with code #{response.code} and message: #{response.body.message}"
  end
end

class MerchantInfoAggregator
  # returns an array of hashes where each hash specifies a merchant ID and the total amount due

  def initialize; end

  def call
    merchant_list = JSON.parse(ApiClient.get_merchant_list)
    merchant_list.map do |merchant_id|
      transaction_list = JSON.parse(ApiClient.get_transaction_list(merchant_id))
      merchant_iban = transaction_list['iban']
      transaction_amount = sum_transactions(transaction_list)
      {
        iban: merchant_iban,
        amount_in_pence: transaction_amount
      }
    end
  end

  private

  def sum_transactions(transaction_list)
    transactions = transaction_list['transactions']
    transactions_sum = transactions.reduce(0) { |sum, transaction| sum + transaction['amount'] }
    fees_sum = transactions.reduce(0) { |sum, transaction| sum + transaction['fee'] }

    if transactions.count >= transaction_list['discount']['minimum_transaction_count']
      fees_sum = ((100 - transaction_list['discount']['fees_discount']).to_f / 100) * fees_sum
    end

    (transactions_sum - fees_sum).round
  end
end

class CSVExporter
  def initialize; end

  def call
    data = MerchantInfoAggregator.new.call

    CSV.open('payments.csv', 'wb', { headers: data.first.keys }) do |csv|
      csv << data.first.keys
      data.each do |hash|
        csv << hash
      end
    end
  end
end

CSVExporter.new.call
