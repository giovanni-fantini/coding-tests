const express = require('express');
require('./src/models/vehicle');

class Server {
  constructor() {
    this.app = express();
    this.setup();
  }

  run(port) {
    this.server = this.app.listen(port, () => {
      console.log(`server running on port ${port}`);
    });
  }

  setup() {
    this.app.use(express.json());
    //auth setup
    this.app.use((req, res, next) => {
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'GET');
      next();
    });

    //healthcheck route
    this.app.get('/health', (req, res, _next) => {
      res.send('200 - API is healthy');
    });

    // API route
    this.app.use('/vehicle', require('./src/routes/vehicles'));

    //error handling
    this.app.use((error, req, res, _next) => {
      console.error(error);
      const status = error.statusCode || 500;
      const message = error.message;
      res.status(status).json({ message: message });
    });
  }
}

module.exports = Server;