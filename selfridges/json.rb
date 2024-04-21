# let input = require('./json_example.json')

# function parse_json(json) {
#   let output = []

#   json.forEach((item) => {
#     console.log(output)
#     console.log(item['price'])
#     obj = {"name": item['name'], "filename": item['filename'], "rating": item['rating'], "price": item['price']}
#     if (output.length == 0 || item['price'] > output[0]['price']) {
#       output.unshift(obj)
#       return
#     }
#     output.push(obj)
#   })
#   return output
# }

# console.log(parse_json(input))

require 'json'
require 'pry-byebug'

def parse_json
  file = File.read('json_example.json')
  input = JSON.parse(file)

  input.map do |blob|
    { price: blob['price'] }
  end.sort_by { |h| h[:price] }
end

p parse_json
