const controller = require('../controllers/vehicles');
const router = require('express').Router();

/**
* @api {get} /vehicles/:id?timestamp=:timestamp 
* @apiName Get vehicle by id and stateLog timestamp
* @apiPermission everyone
*
* @apiParam  {String} [id] id
* @apiParam  {Query} [timestamp] Timestamp of stateLog in shape 'YYYY-MM-DDTHH:MM:SSZ' 
*
* @apiSuccess (200) {Object} mixed `Vehicle` + `stateLog` object
*/

router.get('/', controller.validate('getVehicleByStateLogTimestamp'), controller.getVehicleByStateLogTimestamp);

module.exports = router;