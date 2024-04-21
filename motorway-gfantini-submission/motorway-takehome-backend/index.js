const sequelize = require('./src/db');
const config = require('./src/config/index');
const Server = require('./server');

const server = new Server();

sequelize
  .sync()
  .then(_result => {
    console.log('Database connected');
    server.run(config.port);
  })
  .catch(err => console.error(err));