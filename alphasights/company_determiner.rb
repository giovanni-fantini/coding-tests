require 'json'
require 'pry'

class ResponseHandler
  def initialize(api_response)
    @api_response = api_response
  end

  def call
    hash_obj = JSON.parse(api_response)
    company = Company.new(name: hash_obj["company_name"], public: hash_obj["public"])

    if hash_obj.key?('children')
      hash_obj['children'].each do |child|
        child_company = Company.new(name: child["company_name"], public: child["public"])
        company.assign_child(child_company)

        if child.key?('children')
          child['children'].each do |child2|
            child_company_level2 = Company.new(name: child2["company_name"], public: child2["public"])
            child_company.assign_child(child_company_level2)
          end
        end
      end
    end
    binding.pry
    company
  end

  private

  attr_reader :api_response
end

class Company
  attr_reader :name, :public, :children

  def initialize(name:, public:)
    @name = name
    @public = public
    @children = []
  end

  def assign_child(child)
    @children << child
  end

  def is_public?
    children.flatten.any? { |child| child.public }
  end
end

test_object = '{
  "company_name": "Alphabet",
  "public": false,
  "children": [
    {
      "company_name": "Google US",
      "public": false
    },
    {
      "company_name": "Google Mobile",
      "public": false,
      "children": [
        {
          "company_name": "Android",
          "public": false
        },
        {
          "company_name": "Waze",
          "public": true
        }
      ]
    },
    {
      "company_name": "Google UK",
      "public": false
    }
  ]
}'

puts ResponseHandler.new(test_object).call.is_public?