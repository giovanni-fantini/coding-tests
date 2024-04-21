require 'csv'

module LogHandler
    module Parser
        class Csv < Base
            DEFAULT_SEPARATOR = ' '
            
            def initialize(filepath, col_sep)
                super
                @col_sep = col_sep || DEFAULT_SEPARATOR
            end

            def call(&block)
                parse(&block)
            end

            private 

            attr_reader :file, :col_sep

            def parse
                result = {}

                CSV.foreach(file, col_sep: col_sep) do |row|
                    result = yield(row, result)
                end

                result
            end
        end
    end
end