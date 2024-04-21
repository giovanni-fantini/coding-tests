const Sequelize = require('sequelize');
const StateLog = require('../models/stateLog');
const Vehicle = require('../models/vehicle');
const Op = Sequelize.Op;
const { query, validationResult } = require('express-validator')

exports.validate = (method) => {
  switch (method) {
    case 'getVehicleByStateLogTimestamp': {
     return [ 
        query('vehicleId', 'value provided is not an Int').isInt(),
        query('timestamp', 'value provided is not a Datetime').isISO8601().toDate()
       ]   
    }
  }
}


exports.getVehicleByStateLogTimestamp = (req, res, _next) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
        return res.status(422).json({ errors: errors.array() });
    }
    
    const vehicleId = req.query.vehicleId;
    const timestamp = req.query.timestamp;

    Vehicle.findOne({
        attributes: ['id', 'make', 'model'],
        where: { 
            id: vehicleId 
        },
        include: {
            model: StateLog,
            attributes: ['state', 'timestamp'],
            where: {
                timestamp: {
                    [Op.lt]: new Date(timestamp)
                }
            },
        },
        order: [[{ model: StateLog  }, 'timestamp', 'DESC']]
    })
        .then(vehicle => {
            if (!vehicle) {
                return res.status(404).json({ message: 'No vehicle matching this id AND with state logged before this timestamp was found!' });
            }
            res.status(200).json({ vehicle: vehicle });
        })
        .catch(err => console.error(err));
}