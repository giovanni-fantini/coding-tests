# Utility Coding Challenge

This is Giovanni Fantini's submission for the utility coding challenge.
The instruction file as received via email is found in the root of this directory: *instructions.pdf*.

## Solution Description

The provided solution is a simplistic Django Web Application which has been designed to follow Object Oriented Programming (OOP) notions with immaginary internal staff as final users. The goal of the 'readings' app within the Django project is to offer such staff a way to import meter readings from so called 'flow files', an example of which is found in the test directory.

A few points worth noting:
- There are numerous improvements that could be made to this app, however given the 3h allotment of time I had elected to focus on understanding the requirements and data modelling, putting together a user-friendly working solutions with some tests and writing down proper documentation in this Readme file rather than for instance stronger / safer parsing logic. The improvements I envisaged can be found in the apposite section 
- Most of my work in the last year has been in Ruby so my code might reflect Ruby's style and appear odd to a daily Python consumer
- The solution handles environment segregation and dependency management with pipenv (e.g. Pipfile)
- The solution has been designed and implemented to be locally runnable in a dev environment, without any concern for eventual production deployments (e.g. filepaths are assumed to be universally accessible and user credentials are seeded and shown in plain text)
- As such the data layer is handled by locally-available Sqlite3 
- The solution attempts reusing Django's existing functionality as much as possible
- The solution offers interactivity by means of custom management commands and Django's admin site
- Models have been designed to lay out in the most concise way the domain outlined by the problem description
- The only suggestion I'd give to improve the challenge description is to give some more context on the flow files as candidates can lose a lot of time figuring that out. For instance, I went into a rabbit hole trying to understand how to parse .uff files (attempted using a variety of library)

### Description of the key files (in the readings app)

- **management/commands/createstaffuser.py** it's a custom management command allowing for the creation of an admin user possessing only the required permissions to execute the desired actions as per instructions
- **management/commands/parseflowfiles.py** is the key command allowing said admins to import locally available flow files with meter readings information into the web app, for displaying on the admin site. 
In the current simplistic implementation it doesn't offer much input validation aside from file existence checks, it otherwise assumes these files are all text-like and parsable. This would obviously need to be strongly improved in a production implementation
- **utils.py** contains the actual parsing / importing logic for the abovementioned command. The logic has been encapsulated here as the instructions required extendability of the functionality to a future REST API
- **models.py** contains the data models for the app - *Meter* and *Reading*
- **admin.py** contains the customisation behaviour for the admin site: it sets the permissions for Reading model and makes it searchable
- **tests/** contains some tests for the implementation as well as a flow file fixture. Given the available time I have focused on offering only high-level integration tests of the core importing functionality while deferring detailed unit tests of all its components. Particularly, while mostly relying on highly reliable Django functionality, none of the admin customisation has been tested
- **tests/DTC5259515123502080915D0010.uff** is the sample flow file provided. It has been interpreted to the best of my ability following the suggested DTS documentation but not everything was clear to me (e.g. meaning of first and last line of the file). Couple important assumptions on the data: i) timestamps are assumed to be in UTC; ii) the latest reading is assumed to be the correct one in case of multiple existing for same meter and timestamp.

## To Do Next

A few things I would have implemented next in case of continued work on the program:

0) Add docstrings in the code - I didn't do this as most info was covered in this readme
1) Implementing stronger / safer parsing logic in non-happy path scenarios:
- Checks and exception raising when input files being text and processable by CSV utility
- Checks and exception raising on data shape and types (e.g. mpan being a non-integer)
- Checks and exception raising on data inconsistencies (e.g. that a serial number is always associated with same mpan or that no objects with partial data like absent serial_number are retained)
- Transaction rollbacking when any such major exception is raised
- Rescue exceptions instead of stopping data processing and report number / types of errors analytics in some logs at the end
2) Improving tests: 
- Improving coverage by adding unit tests for each component
- Handling additional non-happy path scenarios
3) Performance improvements:
- Explore need for DB indexing to speed up queries in parsing script
- Explore parallelisation of parsing task
3) Feature improvements on the management commands like:
- Enforcing pending migrations checks
- Creating additional staff users rather than just exiting if one already exists
- Adding more metrics to the output of the main task, such as the number of readings succesfully imported, number of errors / issues etc.

## Installation and runtime
### Requirements
- Python >= 3.10
- pip
- pipenv

### Extract files and navigate to them:
```sh
tar -xf gf_utility_parse_and_display.tar.gz
cd gf_utility_parse_and_display
```

### Create virtual env, install dependencies and activate the env with pipenv:
```sh
pipenv install
pipenv shell
```

### Migrate db:
```sh
python manage.py migrate
```

### Create permissioned user to access admin site:
```sh
python manage.py createstaffuser
```
This command will create a user with lower permissions vs the regular superuser to access the admin site with following credentials: username=admin, password=admin.

### Import readings from a flowfile:
```sh
python manage.py parseflowfiles path_to_file_1.uff path_to_file_2.txt
```
This is the core command for the submission. It accepts multiple paths to files as arguments. To use the provided sample file, you can run:
```sh
python manage.py parseflowfiles readings/tests/DTC5259515123502080915D0010.uff
```

### Start Django server and visualise results on admin site:
```sh
python manage.py runserver
```
Then head over to http://127.0.0.1:8000/admin/readings/reading/, login using the abovementioned credentials (user=admin, password=admin) and you will see all the imported meters reading. You can inspect each of them for further details including the source file and you can use the search bar above to filter by MPAN or meter serial number.

### Run tests:
```sh
python manage.py test readings/tests
```