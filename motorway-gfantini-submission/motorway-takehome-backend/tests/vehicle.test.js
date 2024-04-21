const request = require('supertest');
const Server = require('../server');
const fs = require('fs')
const db = require('../src/db')

const seedQuery = fs.readFileSync('./migrations/01_init.sql', {
  encoding: 'utf-8'
})

beforeAll(() => {
  return db.query(seedQuery);
});

afterAll(() => {
  db.query('DROP TABLE vehicles');
});

describe('getVehicleByStateLogTimestamp', () => {
  const { app } = new Server();
  it('returns 404 & error message when no statelogs before the provided timestamp are available for the vehicle', async () => {
    const res = await request(app).get('/vehicle?vehicleId=2&timestamp=2022-09-10T14:30:00Z');

    const expected = {"message":"No vehicle matching this id AND with state logged before this timestamp was found!"}
    expect(res.statusCode).toEqual(404);
    expect(res.body).toMatchObject(expected);
  });

  it('returns 404 & error message when no vehicles with that id are present in db', async () => {
    const res = await request(app).get('/vehicle?vehicleId=4&timestamp=2022-09-10T14:30:00Z');

    const expected = {"message":"No vehicle matching this id AND with state logged before this timestamp was found!"}
    expect(res.statusCode).toEqual(404);
    expect(res.body).toMatchObject(expected);
  });

  it('returns 422 & error message when a non integer vehicleId gets sent', async () => {
    const res = await request(app).get('/vehicle?vehicleId=ciao&timestamp=2022-09-10T14:30:00Z');

    const expected = {
      "errors": [
        {
          "location": "query",
          "msg": "value provided is not an Int",
          "param": "vehicleId",
          "value": "ciao",
        },
      ]
    }
    expect(res.statusCode).toEqual(422);
    expect(res.body).toMatchObject(expected);
  });

  it('returns 422 & error message when a non datetime timestamp gets sent', async () => {
    const res = await request(app).get('/vehicle?vehicleId=2&timestamp=ciao');

    const expected = {
      "errors": [
        {
          "location": "query",
          "msg": "value provided is not a Datetime",
          "param": "timestamp",
          "value": "ciao",
        },
      ]
    }
    expect(res.statusCode).toEqual(422);
    expect(res.body).toMatchObject(expected);
  });

  it('returns 200 & the right object when the vehicle exists and has statelogs in the past', async () => {
    const res = await request(app).get('/vehicle?vehicleId=3&timestamp=2022-09-11T23:50:00Z');

    const expected = {"vehicle":{"id":3,"make":"VW","model":"GOLF","stateLogs":[{"state":"selling","timestamp":"2022-09-11T23:21:38.000Z"}]}}
    expect(res.statusCode).toEqual(200);
    expect(res.body).toMatchObject(expected);
  });

  it('returns 200 & the right object when the last statelog was one second ago', async () => {
    const res = await request(app).get('/vehicle?vehicleId=3&timestamp=2022-09-12T12:41:42Z');

    const expected = {"vehicle":{"id":3,"make":"VW","model":"GOLF","stateLogs":[{"state":"sold","timestamp":"2022-09-12T12:41:41.000Z"}]}}
    expect(res.statusCode).toEqual(200);
    expect(res.body).toMatchObject(expected);
  });
});