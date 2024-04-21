class ElectricityReadingService
    def initialize(readings_store = nil)
        @readings_store = readings_store || Hash.new
    end

    def getReadings(meter_id)
        @readings_store[meter_id]
    end

    def storeReadings(meter_id, readings)
        @readings_store[meter_id] ||= []
        @readings_store[meter_id].concat(readings)
    end

    def getReadingsByRangeDate(meter_id, start_date, end_date)
        readings = getReadings(meter_id)
        return nil if readings.nil?

        readings.select do |reading|
            reading.date >= start_date && reading.date <= end_date
        end
    end
end