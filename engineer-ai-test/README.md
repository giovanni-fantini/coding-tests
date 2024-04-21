# ToyRobot Problem

## Solution Description

The provided solution is a Ruby Command Line Application (CLI) which has been designed to follow Object Oriented Programming (OOP) notions and an architecture based on single purpose service objects and data models. 

A few points worth noting:
- Objects have been designed to lay out the domain outlined by the problem description and to maximise encapsulation and discreteness to avoid them being too tightly coupled
- Implementation has followed Test Driven Development (TDD) principles and all objects present unit tests

### Description of the components

- I have used *User Stories* to come up with the models and methods
- **app.rb** presents the executable
- **command_executor.rb** is a service object holding the core logic of the application. It lays out the interactions of the objects with each other and with the user's input
- **direction.rb** is a simple model holding the state of the cardinal direction and its behaviour
-  **parser.rb** is a service object used by the command_executor to transform the user's input into interpretable commands
- **position.rb** is a simple model holding the coordinates' state and its behaviour
- **table_top.rb** is a model holding the state and behaviour of the table_top. In a future improvement where a necesity to store data / use multiple toy_robots should arise, this model could be improved to become a crude repository
- **toy_robot.rb** is the main data model of the app which holds the state of the toy_robot and its behaviour. This model makes use of *direction* and *position* models

## Setup and runtime

To run the program, please follow the following steps:

1. Unzip the folder
2. `cd engineer-ai-test`
3. `gem install bundler`
will install the dependency manager
4. `bundle install`
will install the testing framework Rspec
5. `rspec spec`
will run all tests and check for program's integrity
6. `ruby lib/app.rb spec/data/test_data.txt`
will run the program against the sample data and return the output in the terminal. The path to another file (following the same data format) can be provided in place of 'test_data.txt'