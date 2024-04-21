# Mars Rover Problem

## Solution Description

The provided solution is a Ruby Command Line Application (CLI) which has been designed to follow Object Oriented Programming (OOP) notions and an architectural pattern inspired by Model-View-Controller (MVC) structures. 


A few points worth noting:
- Large part of the design and implementation has been influenced by my experience as a Rails web developer. While this might not be the best possible approach, I think it's a good synthetisis of the problem requirements and my previous background
- As per MVC architectures, the program exhibits separation of concerns:
  - Its *models* hold the structure and behaviour of the data
  - The *controller* holds the logic dictating how the models interact with each other and with the user
  - For the sake of simplicity and based on the outlined requirements, no *view* has been implemented and the program runs by receiving user input data at the beginning and reporting an output at the end
- Objects have been designed to lay out the domain outlined by the problem description and to maximise encapsulation and discreteness to avoid them being too tightly coupled (to the extent possible) as it would be advisable when writing production-quality, reusable code
- Implementation has followed Test Driven Development (TDD) principles and all objects present unit tests

### Description of the components

- As a web dev, I have used *User Stories* to come up with the models and methods
- **app.rb** presents the executable script
- **controller.rb** as explained above is the brain of the program describing the interactions of the models with each other and with the user input. It already is capable of handling some edge cases (such as a rover attempting to move out of the plateau's boundaries or in the same position of another rover)
- **direction.rb** is a simple model holding the state of the cardinal direction and its behaviour
-  **parser.rb** is a utility object used by the controller to transform the user's input into interpretable data
- **plateau.rb** is a model holding the state and behaviour of the plateau. It also acts as a repository for the rovers storing their information in an array during runtime; while this causes a closer coupling with the *rover model* this architectural decision sets the base to easily transition the program towards a runnable app if extended with a view, a router and persistent memory (database)
- **position.rb** is a simple model holding the coordinates' state and its behaviour
- **rover.rb** is the core model of the program which holds the state of the rover and its behaviour. This model makes use of *direction* and *position* models


## To Do Next

A few things I would have implemented next in case of continued work on the program:

- Implementing a view, router and database to transition the program towards a runnable app with a user interface and persistent memory
- Inserting the possibility to provide different kinds of input (i.e. via command line or other file types)
- Implementing input validations 
- Handling additional edge cases 
- Improving test coverage
- Functional testing for the app

## Setup and runtime

To run the program, please follow the following steps:

0. `ruby -v` 
will check what if and what version of Ruby is installed on the machine - solution has been written using v2.6.2
1. `unzip solution_fantinig`
2. `cd mars_rover_problem`
3. `gem install bundler`
will install the dependency manager
4. `bundle install`
will install the testing framework Rspec
5. `rspec spec`
will run all tests and check for program's integrity
6. `ruby lib/app.rb sample_data.txt`
will run the program against the sample data and return the output in the terminal. The path to another file (following the same data format) can be provided in place of 'sample_data.txt'