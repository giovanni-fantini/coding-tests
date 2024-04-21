const Sequelize = require('sequelize');
const config = require('../config/index');

const sequelize = new Sequelize(
    config.db.name,
    config.db.user,
    config.db.password,
    {
        host: config.db.host,
        dialect: 'postgres',
        // should be set depending on deployment infra resourcing
        pool: {
            max: 10,
            min: 0,
            idle: 10000
          }
    },
);
console.log('db config');
console.log(config.db);

module.exports = sequelize;