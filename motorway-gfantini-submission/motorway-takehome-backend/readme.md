# Motorway Coding Challenge

This is Giovanni Fantini's submission for the Motorway coding challenge. Date submitted 20/02/23.
The link to the instruction file received via email is found [here](https://motorway.notion.site/Senior-Backend-Engineer-Tech-Challenge-6e59f0edc5d942b0a591a2b1aa248b3f).

## Solution Description

The provided solution is a simple REST API implemented with Node.js, Express as middleware and Sequelizer as an ORM - it's purpose is to offer an interface to retrieve a vehicle's information and state at a particular point in time. The solution employs OOP design, an MVC architecture (without view layer) has been designed to **partial** production-readiness, with a few elements of scalability, reliability and observability in mind. Further below in the "Next steps" section I talk about a few points I felt were out of scope for this task but that would be important to address ahead of a full deployment.

A few points worth noting:
- The solution has been designed and implemented to be runnable in complete isolation via Docker containerization independently of deployment choices / medium, however the testing setup has been designed exclusively for local use
- The boilerplate code has been adjusted to better fit this full containerisation approach
- The solution can be utilised by regular HTTP request tooling (such as CURL commands or Postman clients)
- Models have been designed to lay out in the most concise way the domain outlined by the problem description
### Overview of app files

- */migrations/01_init.sql* contains the SQL code to bring up the database
- */config* contains the configuration mappings required for the data layer
- */controllers/vehicles.js* contains the core logic powering the API, at it's heart is an SQL query joining the two tables and applying where clauses on the two param fields vehicle id and stateLog timestamp
- */db/index.js* contains the setup and instantiation of the ORM
- */models* contains the data models for the app - *Vehicle* and *StateLog* (1-to-Many relationship). A BTREE index has been applied to the stateLog timestamp in an early scalability effort
- */routes* contains the mapping from route to controller action

- *index.js* and *server.js* together hold the setup for Express and the server

- *tests/vehicles.test.js* contains tests covering the 4 cases obviously apparent from the sample data: given data querying is the key of this API I opted for an approach that sets up an actual test DB rather than mocking the calls, to provide some degree of integration testing with the data layer
- */test_support* provides a script to setup the testing database in local and the definition of a load test for the API, given the brief seemed to particularly care about performance assessments

## Next steps

A few things worth considering / doing to make this production-ready, but beyond scope in this exercise:

AROUND INPUT
- Ensure Sequelize prevents SQL injection
- Better error handling in edgecases

AROUND THE DATA LAYER
- Tailor the connection pooling logic
- Investigate caching layer even thogh allowing to query by granular timestamp (up to the millisec) defeats standard request caching
- Indexing is done aggressively when Sequelize syncs. This is dangerous for long indexing procedures and should be rearchitected to go in migrations

AROUND REQUEST HANDLING (PROBABLY PERFORMED BY A REVERSE PROXY)
- Add Auth checks and handling
- Add logic to power orchestration engines
- Add load balancing

OTHER
- Fix dependency alerts and investigate alternative tooling

## Installation and runtime
### Requirements
- node.js ~ LTS/hydrogen
- npm
- postgres
- docker

### Extract files and navigate to them:
```sh
tar -xf motorway-gfantini-submission.tar.gz
cd motorway-gfantini-submission/motorway-takehome-backend
```

### Launch the app in docker:
```sh
(sudo) docker compose up --build
```
If a ConnectionRefusedError gets raised by Docker, run the command again without building after stopping the docker instances with Ctrl / Cmd + C:
```sh
docker compose up
```

### Send requests to the API and inspect responses:
Example:
```sh
curl http://localhost:3000/vehicle\?vehicleId\=3\&timestamp\=2022-09-12T12:41:42Z
> {"vehicle":{"id":3,"make":"VW","model":"GOLF","stateLogs":[{"state":"sold","timestamp":"2022-09-12T12:41:41.000Z"}]}}
```

### Install the app locally:
```sh
npm install
```

### Prepare and run integration tests:
```sh
npm run setup_tests
npm test
```

### Run load test:
Ensure you have docker still running:
```sh
docker compose up
```
Then:
```sh
npm run load_test_api
```