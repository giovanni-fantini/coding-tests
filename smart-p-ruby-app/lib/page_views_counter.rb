module LogHandler
    class PageViewsCounter
        def self.call(row:, result:)
            new(row, result).call
        end

        def initialize(row, result)
            @row = row
            @result = result
        end

        def call
            count_page_views
            result
        end

        private

        attr_reader :row, :result

        def count_page_views
            result.has_key?[page] ? ip_address_count : result[page] = {}
        end

        def ip_address_count
            result[page].has_key?(ip_address) ? result[page][ip_address] += 1 : result[page][ip_address] = 1
        end

        def page
            @page ||= row[0]
        end

        def ip_address
           @ip_address ||= row[1]
        end
    end
end