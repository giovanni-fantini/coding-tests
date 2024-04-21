class ParseResponse
  def initialize(raw_json)
    @raw_json = raw_json
  end
 
  def call
    json = JSON.parse(raw_json)
    output = json.map do |item|
      { title: item["title"], price: item["price"], category: item["category"] }
    end
    output.sort_by! { |item| item[:price] }
    output.select { |item| item[:category] == 'electronics' }
  end
 
  private
 
  attr_reader :raw_json
end