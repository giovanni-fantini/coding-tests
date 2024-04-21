# Homey Coding Challenge

This is Giovanni Fantini's submission for Homey's coding challenge. Date submitted 09/03/23.
The link to the instructions received is [here](https://allentities.notion.site/Task-Development-Team-d5aae74100544f84981972edb3d922b0).

## Solution Description

The provided solution is a simple REST API implemented with Ruby on Rails - it's purpose is to offer an interface for a user to interact with a project, being able to leave comments for it and changing the project's status. The solution employs OOP design, an MVC architecture and has been designed to favour transparency and code clarity over scalability and performance, presuming the application to be a low traffic one. Further below in the "Next steps and other considerations" section I talk about a few points I felt were out of scope for this task but would have been important to address IRL.

## Imagined Q&A
As per the instructions, here by an assumed Q&A with some other internal stakeholder:
### Questions around the domain modelling
- What kind of traffic volume are we expecting for the website? Should we favour performance or code clarity?
We should assume low traffic and wherever possible favour transparent, readable code over extra performance
- User requirements, auth and admin functionality
We should assume a simple User model based on email / password authentication. Login only required to update a project and leave a comment, viewing resources is open to everyone. No admin functionality
- To this extent should we restrict Projects by user?
At the moment we'll consider projects being unattached to users. Any user can access / modify any project as long as they're logged in
- What are the available statuses for Projects and are there invalid transitions of status?
Assume available statuses are 'Not started', 'In progress', 'Done' and there are no invalid transitions at this moment in time
- Should we allow comments or status changes with missing attributes?
No, all interactions should require a body, user and project to be valid

### Around routes and controllers
- What endpoints should our API expose?
Assume the landing page to list all the projects, allowing the user to select one and view the project comments and status changes history
- Should we have one route and view for each controller action?
Favour a one-page application approach where comments and status changes can be performed directly on the Project show page

### Around frontend
- Are you fine with a miserable frontend? :D
Yes, please provide a simple user interface
- Can we use an approach for fully static pages?
Yes

### Around frontend
- What testing framework should I use?
Please use RSpec
- What approach to testing should I favour?
Please favour testing behaviour over implementation, and where possible integration over isolated units
- So should I opt for requests specs instead of controller specs?
Yes
## Next steps and other considerations

A few things worth noting or addressing if this project was worked additionally:

- The app has been generated with `rails new --minimal` to keep it as streamlined as possible, hence all additional features and JS are not available
- Devise has been used to handle the User domain and simplistic authentication
- StatusChange has been modelled to keep track of project status changes for the sake of simplicity, IRL we might have explored using PaperTrail which is a gem allowing for auditing of models and tracking their changes through time
- Indexing is added by default to `project_id` as a foreign key in Comment and StatusChange which we want to keep as these resources are queried by project. I manually removed indexing from the `user_id` keys as currently unnecessary
- Code clarity has been favoured over performance: for example in the `interaction_history` method in the Project model I chose to query the db through Active::Record (which queries the DB twice) and sort in-memory instead of querying and sorting directly in one single, complex SQL query
- Behaviour testing has been favoured over implementation and not every single unit has been tested insolation as beyond scope and time. Major flows and scenarios have been tested for with request specs

## Installation and runtime
### Requirements
- ruby 3.2.1
- rails 7
- bundler
### Clone this repository:
```sh
git clone git@github.com:giovanni-fantini/homey-tech-test.git
cd homey-tech-test
```

### Install dependencies:
```sh
bundle install
```

### Setup the database:
```sh
bundle exec rails db:create db:migrate db:seed
```

### Launch the app server:
```sh
./bin/dev
```

### Navigate the app:
- Navigate to the [app](localhost:3000)
- Click on "Homey tech test"
- You can see the first two project elements that were seeded in the database, ordered by time
- Try adding a new comment with the form at the bottom of the page
- You'll be redirected to login. Use 'gio@example.com' and 'password' as credentials or create another user
- Feel free to play around adding more comments or updating the status with the forms provided at the bottom of the project history page

### Running tests:
```sh
bundle exec rspec spec
```