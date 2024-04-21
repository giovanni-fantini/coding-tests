# Auction Simulator Task

This is Giovanni Fantini's submission for Thought Machine's task.
The instruction brief as received is found in the root of this directory: *task_brief.md*.

## Solution Description

The provided solution is a simplistic CLI application which has been designed to follow Object Oriented Programming (OOP) notions. The goal of the app is to offer users a way to import sell & bid instructions describing auctions from a pipe-delimited files (examples are found in the fixtures directory) and have the program output the outcome of each auction based on the sequence of such instructions.

A few points worth noting:
- There are improvements that could be made to this app, however given the allotment of time I have elected to focus on good object design, testing coverage and documentation with a decently solid parsing logic. A few improvements I envisaged can be found in the apposite section below
- The solution attempts making use of classes partially replicating standard behaviour for data models in object-oriented apps, such as models associations and validation callbacks on object save. Please see class docstrings for further detail
- The code and the logic could have been greatly simplified with the use of third-party libraries, but as requested in the bried I resorted only to Python's standard library
- A lot of my work in the last year has been in Ruby so there may be syntactical choices which could seem less Pythonic
- The solution handles environment segregation and dependency management with pipenv (e.g. Pipfile)
- The solution has been designed and implemented to be locally runnable in a dev environment, with many simplified assumptions (e.g. filesystem paths are assumed to be universally accessible)
## To Do Next

A few things I would have implemented next in case of further time available for the task / continued work on the program:

1) Improve the parsing logic:
- Add support for other delimiters
- Better error displaying with context of where in the file the error occured
- Accept multiple files at once
2) Improving tests:
- Improving coverage by adding more edge case scenarios
- DRY up by mocking and sharing contexts
3) Improve files and directory structure to follow a classic Python package approach
- Consequentially improve / centralise the way imports are handled 

## Installation and runtime
### Requirements
- Python >= 3.10
- pip
- pipenv

### Extract files and navigate to them:
```sh
tar -xf gf_auction_test.tar.gz
cd gf_auction_test
```

### Create virtual env, install dependencies and activate the env with pipenv:
```sh
pipenv install
pipenv shell
```

### Run the app against a test json file:
```sh
python main.py path_to_file.txt [-v]
```
This is the core command for the submission. It currently accepts one path as argument. It also accepts the `-v` option to include outputting DEBUG statements such as row validation errors.

To use the sample provided in the instructions, you can run:
```sh
python main.py fixtures/input.txt
```
### Run tests:
```sh
python -m unittest discover .
```
