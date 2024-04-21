import csv
import os
from datetime import datetime, timezone
from readings.models import Meter, Reading

class MalformedDataError(Exception):
    pass

def import_flowfile(file):
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        meter = Meter()
        reading = Reading()
        for row in reader:
            if row[0] == '026':
                mpan = int(row[1])
                meter = Meter.objects.get_or_create(mpan=mpan)[0]
                next
            elif row[0] == '028':
                serial_number = row[1]
                if bool(meter.serial_number):
                    if not meter.serial_number == serial_number:
                        raise MalformedDataError(f'Conflicting serial numbers provided for mpan: {meter.mpan}')
                    else:
                        next

                meter.serial_number = serial_number
                meter.save()
                next
            elif row[0] == '030':
                timestamp = datetime.strptime(row[2], '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
                reading = Reading.objects.get_or_create(meter=meter, datetime=timestamp)[0]
                reading.value = float(row[3])
                filename = os.path.basename(os.path.normpath(file))
                reading.source = filename
                reading.save()
                next
