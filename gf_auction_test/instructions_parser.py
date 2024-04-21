import csv
import logging
from auction import Auction
from bid import Bid
from heartbeat import Heartbeat


class InstructionsParser:
    """A class to import instructions from txt files into memory, to allow execution.
    Edge cases the parser guards against:
        - File not tab delimited
        - Empty file
        - Timestamps of rows not strictly increasing
        - Unrecognized instructions (i.e not maching any provided specification)
        - Row columns do not match expected data types

    Attributes:
        input_file (str): a string representing the filepath to the input file to be imported

    Methods:
        call():
            Executes the import of the file
    """

    def __init__(self, input_file):
        self.input_file = input_file
        self.instructions = []
        self.last_timestamp_processed = 0

    def call(self):
        """Executes the import of the file

        Returns:
            list: a list of the imported instructions which had a valid form
        """
        with open(self.input_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="|")
            for row in reader:
                self._validate_and_import_instruction(row)
            return self.instructions

    def _validate_and_import_instruction(self, row):
        try:
            if self.last_timestamp_processed >= int(row[0]):
                logging.debug(
                    "Instruction's timestamp is not stricly increasing, skipping line"
                )
            elif len(row) == 6 and row[2] == "SELL":
                self.instructions.append(
                    Auction(
                        timestamp=int(row[0]),
                        user_id=int(row[1]),
                        item=row[3],
                        reserve_price=float(row[4]),
                        closing_time=int(row[5]),
                    )
                )
            elif len(row) == 5 and row[2] == "BID":
                self.instructions.append(
                    Bid(
                        timestamp=int(row[0]),
                        user_id=int(row[1]),
                        item=row[3],
                        bid_amount=float(row[4]),
                    )
                )
            elif len(row) == 1:
                self.instructions.append(Heartbeat(timestamp=int(row[0])))
            else:
                logging.debug("Unknown instruction provided, skipping line")

            self.last_timestamp_processed = int(row[0])
        except ValueError as error:
            logging.debug(
                f"Malformed instruction provided, skipping line. Raised error: {error}"
            )
