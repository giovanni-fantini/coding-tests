from io import StringIO
import datetime
import unittest
from unittest.mock import patch
from freezegun import freeze_time
from json_parser import JsonParser
from person import Person
from birthday_determiner import BirthdayDeterminer
from main import main


class JsonParserTestCase(unittest.TestCase):
    def setUp(self):
        self.input_file = "fixtures/provided_sample.json"

    def test_data_is_imported_as_a_list_of_tuples_with_right_types(self):
        """Tests .call() imports JSON correctly and returns a list of typed tuples"""
        tuples = JsonParser(self.input_file).call()
        self.assertEqual(len(tuples), 4)
        last_tuple = tuples[-1]
        self.assertIsInstance(last_tuple, tuple)
        self.assertEqual(last_tuple[0], "Curry")
        self.assertEqual(last_tuple[1], "Mark")
        self.assertEqual(last_tuple[2], datetime.datetime(1988, 2, 29, 0, 0))

    def test_success_message_is_printed(self):
        """Tests that a success message is printed at the end of the import"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            JsonParser(self.input_file).call()
            self.assertEqual(
                fake_out.getvalue(), "JSON parsed succesfully. 4 birthdays imported\n"
            )

    def test_malformed_json_not_imported(self):
        """Tests malformed JSON files are not imported"""
        output = JsonParser("fixtures/malformed_json_test.json").call()
        self.assertEqual(len(output), 0)

    def test_malformed_json_prints_message(self):
        """Tests malformed JSON files cause the class to print an error message"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            JsonParser("fixtures/malformed_json_test.json").call()
            self.assertEqual(
                fake_out.getvalue(),
                "JSON file could not be loaded, please check format is correct.\n",
            )

    def test_invalid_data_types_not_imported(self):
        """Tests rows with invalid data types in the JSON are not imported"""
        tuples = JsonParser("fixtures/invalid_types.json").call()
        self.assertEqual(len(tuples), 1)
        last_tuple = tuples[-1]
        self.assertIsInstance(last_tuple, tuple)
        self.assertEqual(last_tuple[0], "Tester")
        self.assertEqual(last_tuple[1], "Pro")
        self.assertEqual(last_tuple[2], datetime.datetime(2020, 1, 1, 0, 0))

    def test_invalid_data_types_print_validation_errors(self):
        """Tests rows with invalid data types in the JSON are flagged to the user"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            JsonParser("fixtures/invalid_types.json").call()
            output = fake_out.getvalue()
            self.assertIn("False is not of type 'datetime'", output)
            self.assertIn("1 is not of type 'string'", output)

    def test_invalid_dates_not_imported(self):
        """Tests rows with invalid dates in the JSON are not imported"""
        tuples = JsonParser("fixtures/invalid_dates.json").call()
        self.assertEqual(len(tuples), 0)

    def test_invalid_dates_print_validation_errors(self):
        """Tests rows with invalid dates in the JSON are flagged to the user"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            JsonParser("fixtures/invalid_dates.json").call()
            output = fake_out.getvalue()
            self.assertIn("'2023/02/29' is not of type 'datetime'", output)


class PersonTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @freeze_time("2023-03-21")
    def test_isbirthday_works(self):
        """Tests the .isbirthday() helper method returns True when the Person's birthday is today"""
        bday_person = Person("Tester", "Pro", datetime.datetime(1990, 3, 21, 0, 0))
        self.assertEqual(bday_person.isbirthday(), True)
        non_bday_person = Person("Tester", "Pro", datetime.datetime(1990, 3, 22, 0, 0))
        self.assertEqual(non_bday_person.isbirthday(), False)

    @freeze_time("2023-02-28")
    def test_isbirthday_works_for_leap_birthdays(self):
        """Tests the isbirthday helper method works for people born on 29th Feb"""
        bday_person = Person("Tester", "Pro", datetime.datetime(2020, 2, 29, 0, 0))
        self.assertEqual(bday_person.isbirthday(), True)
        non_bday_person = Person("Tester", "Pro", datetime.datetime(1990, 3, 22, 0, 0))
        self.assertEqual(non_bday_person.isbirthday(), False)


class BirthdayDeterminerTestCase(unittest.TestCase):
    def setUp(self):
        self.list_of_people = [
            Person("Doe", "John", datetime.datetime(1982, 10, 8, 0, 0)),
            Person("Curry", "Mark", datetime.datetime(1988, 2, 29, 0, 0)),
            Person("Average", "Joe", datetime.datetime(1987, 2, 28, 0, 0)),
        ]

    @freeze_time("2023-02-28")
    def test_it_outputs_the_right_subset_of_people(self):
        """Tests .call() outputs the right list of people whose birthday is today"""
        output = BirthdayDeterminer().call(self.list_of_people)
        expected_output = self.list_of_people[-2:]
        self.assertEqual(output, expected_output)

    @freeze_time("2023-02-28")
    def test_it_prints_the_subset_of_people(self):
        """Tests it prints thelist of people to console"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            BirthdayDeterminer().call(self.list_of_people)
            output = fake_out.getvalue()
            self.assertEqual(
                "Today's birthdays are:\nMark Curry\nJoe Average\n", output
            )

    @freeze_time("2023-01-01")
    def test_no_birhdays_output_nothing(self):
        """Tests .call() outputs nothing when there are no birthdays"""
        output = BirthdayDeterminer().call(self.list_of_people)
        self.assertEqual(output, [])

    @freeze_time("2023-01-01")
    def test_no_birthdays_output_message(self):
        """Tests it prints thelist of people to console"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            BirthdayDeterminer().call(self.list_of_people)
            output = fake_out.getvalue()
            self.assertEqual("There are no birthdays today.\n", output)


class MainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @freeze_time("2023-02-28")
    def test_integration(self):
        """Tests the integration of the components from user input to output"""
        filepath = "fixtures/provided_sample.json"
        with patch("sys.argv", ["main.py", filepath]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("JSON parsed succesfully. 4 birthdays imported\n", output)
                self.assertIn("Today's birthdays are:\nMark Curry\n", output)

    def test_invalid_filepath(self):
        """Tests the early exit of the program when filepath is invalid"""
        filepath = "fixtures/unexistent.json"
        with patch("sys.argv", ["main.py", filepath]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertEqual(
                    "JSON file not found, please provide a valid filepath.\n", output
                )


if __name__ == "__main__":
    unittest.main(buffer=True)
