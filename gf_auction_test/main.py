import argparse
import sys
import logging
from pathlib import Path
from auction import Auction
from bid import Bid
from instructions_parser import InstructionsParser


def main():
    """Runs the program. It can be called from command line using the following syntax:
    `$ python main.py filepath [--verbose]`
    To run the program against the supplied input:
    `$ python main.py fixtures/input.txt`

    CommandLine Args:
        filepath: the path to the file containing the instructions to be imported
        --verbose: a flag that can be set to have the program output DEBUG level messages
        (e.g. for rows failing validations)
    """
    parser = argparse.ArgumentParser(prog='auction_simulator', description='Simulates outcomes of auctions based on the instructions provided in the filepath')
    parser.add_argument("filepath", type=Path)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.filepath.exists():
        instructions = InstructionsParser(args.filepath).call()
        for instruction in instructions:
            _handle_instruction(instruction)
            auctions_to_be_closed = Auction.find_by_closing_time(instruction.timestamp)
            _close_auctions(auctions_to_be_closed)
    else:
        logging.error("File not found, please provide a valid filepath.")


def _handle_instruction(instruction):
    if isinstance(instruction, Auction) or isinstance(instruction, Bid):
        instruction.save()


def _close_auctions(auctions):
    if auctions:
        for auction in auctions:
            auction.close()


if __name__ == "__main__":
    sys.exit(main())
