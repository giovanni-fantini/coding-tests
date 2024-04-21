const Sequelize = require('sequelize');
const db = require('../db');
require('../models/vehicle');

const StateLog = db.define('stateLog', {
    vehicleId: Sequelize.INTEGER,
    state: Sequelize.STRING,
    timestamp: Sequelize.DATE
}, {
    timestamps: false,
    indexes: [
        {
            unique: true,
            fields: ['vehicleId', 'timestamp']
        },
        {
            name: 'timestamp_index',
            using: 'BTREE',
            fields: [
                {
                    name: 'timestamp',
                    order: 'DESC'
                }
            ],
        }
    ]
});
StateLog.removeAttribute('id');

module.exports = StateLog;