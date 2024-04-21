import unittest
from instructions_parser import InstructionsParser
from auction import Auction
from bid import Bid
from heartbeat import Heartbeat


class InstructionsParserTestCase(unittest.TestCase):
    def setUp(self):
        self.input_file = "fixtures/input.txt"

    def test_data_is_imported_and_returned_as_a_list(self):
        """Tests .call() imports input correctly and returns a list of instructions"""
        instructions = InstructionsParser(self.input_file).call()
        self.assertIsInstance(instructions, list)
        self.assertEqual(len(instructions), 10)

    def test_auctions_are_imported_correctly(self):
        """Tests auctions instructions are imported with the right object"""
        instructions = InstructionsParser(self.input_file).call()
        auction = instructions[0]
        self.assertIsInstance(auction, Auction)
        self.assertEqual(auction.timestamp, 10)
        self.assertEqual(auction.user_id, 1)
        self.assertEqual(auction.item, "toaster_1")
        self.assertEqual(auction.reserve_price, 10.0)
        self.assertEqual(auction.closing_time, 20)

    def test_bids_are_imported_correctly(self):
        """Tests bids instructions are imported with the right object"""
        instructions = InstructionsParser(self.input_file).call()
        bid = instructions[1]
        self.assertIsInstance(bid, Bid)
        self.assertEqual(bid.timestamp, 12)
        self.assertEqual(bid.user_id, 8)
        self.assertEqual(bid.item, "toaster_1")
        self.assertEqual(bid.bid_amount, 7.5)

    def test_heartbeats_are_imported_correctly(self):
        """Tests hearbeat instructions are imported with the right object"""
        instructions = InstructionsParser(self.input_file).call()
        heartbeat = instructions[-2]
        self.assertIsInstance(heartbeat, Heartbeat)
        self.assertEqual(heartbeat.timestamp, 20)

    def test_data_not_delimited_by_pipes_is_not_imported(self):
        """Tests rows not delimited by pipes are not imported"""
        instructions = InstructionsParser("fixtures/comma_delimited.txt").call()
        self.assertEqual(len(instructions), 1)
        self.assertIsInstance(instructions[0], Heartbeat)

    def test_data_not_delimited_by_pipes_logs_message(self):
        """Tests rows not delimited by pipes log an error message"""
        with self.assertLogs(level="DEBUG") as logger:
            InstructionsParser("fixtures/comma_delimited.txt").call()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Malformed instruction provided, skipping line. Raised error: invalid literal for int() with base 10: '10,1,SELL,toaster_1,10.00,20'"
                ],
            )

    def test_empty_file_is_processed(self):
        """Tests empty files are imported as an empty list"""
        instructions = InstructionsParser("fixtures/empty.txt").call()
        self.assertEqual(instructions, [])

    def test_instructions_without_increasing_timestamp_are_not_imported(self):
        """Tests rows with a timestamp occurring after a previously processed one are not imported"""
        instructions = InstructionsParser("fixtures/wrong_timestamp.txt").call()
        self.assertEqual(len(instructions), 1)
        auction = instructions[-1]
        self.assertIsInstance(auction, Auction)
        self.assertEqual(auction.timestamp, 10)
        self.assertEqual(auction.user_id, 1)
        self.assertEqual(auction.item, "toaster_1")
        self.assertEqual(auction.reserve_price, 10.0)
        self.assertEqual(auction.closing_time, 20)

    def test_instructions_without_increasing_timestamp_log_message(self):
        """Tests rows with a timestamp occurring after a previously processed one  log an error message"""
        with self.assertLogs(level="DEBUG") as logger:
            InstructionsParser("fixtures/wrong_timestamp.txt").call()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Instruction's timestamp is not stricly increasing, skipping line"
                ],
            )

    def test_unknown_instructions_are_not_imported(self):
        """Tests rows with an unknown structure are not imported"""
        instructions = InstructionsParser("fixtures/unknown_instructions.txt").call()
        self.assertEqual(len(instructions), 1)
        bid = instructions[0]
        self.assertIsInstance(bid, Bid)
        self.assertEqual(bid.timestamp, 12)
        self.assertEqual(bid.user_id, 8)
        self.assertEqual(bid.item, "toaster_1")
        self.assertEqual(bid.bid_amount, 7.5)

    def test_unknown_instructions_log_message(self):
        """Tests rows with an unknown structure log an error message"""
        with self.assertLogs(level="DEBUG") as logger:
            InstructionsParser("fixtures/unknown_instructions.txt").call()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Unknown instruction provided, skipping line",
                    "DEBUG:root:Unknown instruction provided, skipping line",
                ],
            )

    def test_rows_with_wrong_types_are_not_imported(self):
        """Tests rows with wrong data types are not imported"""
        instructions = InstructionsParser("fixtures/wrong_data_types.txt").call()
        self.assertEqual(len(instructions), 1)
        bid = instructions[0]
        self.assertIsInstance(bid, Bid)
        self.assertEqual(bid.timestamp, 12)
        self.assertEqual(bid.user_id, 8)
        self.assertEqual(bid.item, "toaster_1")
        self.assertEqual(bid.bid_amount, 7.5)

    def test_rows_with_wrong_types_log_message(self):
        """Tests rows with wrong data types log an error message"""
        with self.assertLogs(level="DEBUG") as logger:
            InstructionsParser("fixtures/wrong_data_types.txt").call()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Malformed instruction provided, skipping line. Raised error: invalid literal for int() with base 10: 'something'",
                    "DEBUG:root:Malformed instruction provided, skipping line. Raised error: invalid literal for int() with base 10: 'something_else'",
                    "DEBUG:root:Malformed instruction provided, skipping line. Raised error: could not convert string to float: 'False'",
                ],
            )


if __name__ == "__main__":
    unittest.main(buffer=True)
