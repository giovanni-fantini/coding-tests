from io import StringIO
import unittest
from unittest.mock import patch
from main import main
from auction import Auction
from bid import Bid


class MainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        Auction.repository = []
        Bid.repository = []

    def test_integration(self):
        """Tests the integration of the components from user input to output"""
        filepath = "fixtures/input.txt"
        with patch("sys.argv", ["main.py", filepath]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertIn("20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n", output)
                self.assertIn("20|tv_1||UNSOLD|0.00|2|200.00|150.00\n", output)

    def test_invalid_filepath(self):
        """Tests the early exit of the program when filepath is invalid"""
        filepath = "fixtures/unexistent.txt"
        with patch("sys.argv", ["main.py", filepath]):
            with self.assertLogs(level="DEBUG") as logger:
                main()
                self.assertEqual(
                    logger.output,
                    ["ERROR:root:File not found, please provide a valid filepath."],
                )

    def test_no_output_with_empty_file(self):
        """Tests no output is printed when the file is empty"""
        filepath = "fixtures/empty.txt"
        with patch("sys.argv", ["main.py", filepath]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertEqual("", output)

    def test_no_output_with_heartbeat_only_file(self):
        """Tests no output is printed when the file contains only heartbeats"""
        filepath = "fixtures/heartbeats.txt"
        with patch("sys.argv", ["main.py", filepath]):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()
                self.assertEqual("", output)


if __name__ == "__main__":
    unittest.main(buffer=True)
