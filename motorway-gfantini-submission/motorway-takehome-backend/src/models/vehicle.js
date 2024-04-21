const Sequelize = require('sequelize');
const db = require('../db');
const StateLog = require('../models/stateLog');

const Vehicle = db.define('vehicle', {
    id: {
        type: Sequelize.INTEGER,
        autoIncrement: true,
        allowNull: false,
        primaryKey: true
    },
    make: Sequelize.STRING,
    model: Sequelize.STRING,
    state: Sequelize.STRING
}, {
    timestamps: false
});

Vehicle.hasMany(StateLog);
StateLog.belongsTo(Vehicle);

module.exports = Vehicle;