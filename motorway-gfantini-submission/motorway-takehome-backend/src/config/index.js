const convict = require('convict');

const config = convict({
  env: {
    doc: 'The application environment.',
    format: ['prod', 'test'],
    default: 'prod',
    env: 'NODE_ENV',
  },
  port: {
    doc: 'The port to bind.',
    format: 'port',
    default: 3000,
    env: 'PORT',
  },
  db: {
    host: {
      doc: 'Database host name/IP',
      format: '*',
      default: 'postgres',
      env: 'DB_HOST',
    },
    name: {
      doc: 'Database name',
      format: String,
      default: 'motorway',
      env: 'DB_NAME',
    },
    user: {
      doc: 'Database user',
      format: String,
      default: 'user',
      env: 'DB_USER',
    },
    port: {
      doc: 'database port',
      format: 'port',
      // note that this can be overriden depending on what environment you run on
      // please check out local.json and test.json and production.json
      default: 5432,
      env: 'DB_PORT',
    },
    password: {
      doc: 'database password',
      format: '*',
      default: 'password',
      env: 'DB_PASSWORD',
      sensitive: true,
    },
  },
});

const env = config.get('env');
config.loadFile(`./src/config/${env}.json`);
config.validate({ allowed: 'strict' });

module.exports = {
  ...config.getProperties(),
};