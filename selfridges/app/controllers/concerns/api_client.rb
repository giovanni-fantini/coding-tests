class ApiClient
  def initialize(url)
    @url = url
  end
 
  def call
    response = HTTParty.get(url)
    response.to_s
  end
 
  private 
 
  attr_reader :url
end