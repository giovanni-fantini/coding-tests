from io import StringIO
from django.test import TestCase
from django.core.management import call_command, CommandError
from readings.models import Reading
from readings.utils import import_flowfile

class ReadingTestCase(TestCase):
    def setUp(self):
        pass

    def test_readings_can_be_imported(self):
        """Input flowfiles are correctly imported"""
        input_file = 'readings/tests/DTC5259515123502080915D0010.uff'
        import_flowfile(input_file)
        readings = Reading.objects.all()
        self.assertEqual(len(readings), 11)
        last_reading = readings.last()
        self.assertEqual(last_reading.meter.mpan, 2000055433806)
        self.assertEqual(last_reading.meter.serial_number, 'D13C01717')
        self.assertEqual(str(last_reading.datetime), '2016-03-01 00:00:00+00:00')
        self.assertEqual(last_reading.value, 7242.0)
        self.assertEqual(last_reading.source, 'DTC5259515123502080915D0010.uff')

    def test_bad_data_does_nothing(self):
        """Input flowfiles with bad data are processed but nothing happens"""
        input_file = 'readings/tests/sample_bad_data.txt'
        import_flowfile(input_file)
        readings = Reading.objects.all()
        self.assertEqual(len(readings), 0)

class ParseflowfilesTest(TestCase):
    def test_correct_task_output(self):
        out = StringIO()
        call_command(
            'parseflowfiles', 
            'readings/tests/DTC5259515123502080915D0010.uff', 
            'readings/tests/sample_bad_data.txt', 
            stdout=out
            )
        self.assertIn('Task succesfully executed: 2 flow files processed', out.getvalue())

    def test_unexisting_input_file(self):
        with self.assertRaises(CommandError):
            call_command('parseflowfiles', 'unexisting_file.txt')
