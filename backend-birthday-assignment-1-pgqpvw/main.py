import argparse
import sys
from pathlib import Path
from json_parser import JsonParser
from person import Person
from birthday_determiner import BirthdayDeterminer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=Path)
    args = parser.parse_args()

    if args.filepath.exists():
        tuples = JsonParser(args.filepath).call()
        list_of_people = [Person(item[0], item[1], item[2]) for item in tuples]
        BirthdayDeterminer().call(list_of_people)
    else:
        print("JSON file not found, please provide a valid filepath.")


if __name__ == "__main__":
    sys.exit(main())
