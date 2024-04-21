# Birthday Task

This is Giovanni Fantini's submission for Saltpay's task.
The instruction brief as received is found in the root of this directory: *instructions.md*.

## Solution Description

The provided solution is a simplistic CLI application which has been designed to follow Object Oriented Programming (OOP) notions. The goal of the app is to offer users a way to import birthdays from array-formatted JSON files (examples are found in the fixtures directory) and have the program output any people who's birthday falls on that day.

A few points worth noting:
- There are improvements that could be made to this app, however given the allotment of time I have elected to focus on good object design & encapsulation, on testing coverage and on good documentation in this README rather than for instance stronger / safer parsing logic. A few improvements I envisaged can be found in the apposite section below
- The solution favours single purpose classes that attempt to communicate their intent in the class naming and which expose a single publically available API `.call()`
- Most of my work in the last year has been in Ruby so there may be syntactical choices which could be less Pythonic and more Ruby-like
- The solution handles environment segregation and dependency management with pipenv (e.g. Pipfile)
- The solution has been designed and implemented to be locally runnable in a dev environment, without any concern for eventual production deployments (e.g. filepaths are assumed to be universally accessible)

### Description of the files

- **person.py**: this is the basic model for the data, a simple class storing names and date of birthdays and exposing a helper method to determine if that person's birthday is today
- **json_parser.py**: this is the class responsible for parsing the input JSON files, validating their content against the expected schema and handling / displaying any errors there may be. It returns a generally consumable object: a list of tuples - I have specifically elected to not return Person objects to not couple the two classes together
- **birthday_determiner.py**: this class takes a list of people as input and applies a filter to return only those whose birthdays are today, also displaying them to the user
- **main.py**: this is the top-level executable tying together the isolated objects together by chaining their calls. It also provides the functionality to retrieve the input file as a CLI argument from the user

## To Do Next

A few things I would have implemented next in case of continued work on the program:

1) Improve documentation
- Add docstrings in the code. I didn't do this as most info was covered in this readme
- Add in-terminal documentation for the CLI command
2) Add a view layer object to take responsibility on message formatting, printing and all user interactions instead of having that logic spread throughout classes
3) Improve the parsing logic:
- Currently the `datetime` and `jsonschema` libraries share validation responsibility as the latter doesn't handle non-RFC-standard (e.g. YYYY-MM-DD) formats out of the box, so parsing relies on datetime transforming string dates into datetime objects (or raising exceptions when not of any acceptable format) which are then validated by the schema. A natural improvement would be to write a custom validator in jsonschema to handle various date formats validations directly  
- Attempt to refactor the logic to perform the filtering out of invalid rows also through jsonschema instead of being done manually, for instance exploring removing the rows affected by errors in validation callbacks
- Improve final messaging (i.e. add information on invalid rows that were removed)
- Accept multiple JSON files at once
4) Improving tests:
- Improving coverage by adding more edge case scenarios
- DRY up by mocking and sharing contexts
5) Improve files and directory structure to follow a classic Python package approach
- Consequentially improve / centralise the way imports are handled 

## Installation and runtime
### Requirements
- Python >= 3.10
- pip
- pipenv

### Create virtual env, install dependencies and activate the env with pipenv:
```sh
pipenv install
pipenv shell
```

### Run the app against a test json file:
```sh
python main.py path_to_file.json
```
This is the core command for the submission. It currently accepts one path as argument. To use the sample provided in the instructions, you can run:
```sh
python main.py fixtures/provided_sample.json
```
### Run tests:
```sh
python tests.py
```