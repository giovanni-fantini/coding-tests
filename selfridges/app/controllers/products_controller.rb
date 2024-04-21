class ProductsController < ApplicationController
  def index
    url = 'https://fakestoreapi.com/products' 
    response = ApiClient.new(url).call
    render json: ParseResponse.new(response).call.to_json
  end
end