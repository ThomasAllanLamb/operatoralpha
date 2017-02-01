var express = require('express');
var router = express.Router();
var path = require('path');

function api (app) {

  //main page displays a demo of the api
  router.get('/', function(req, res, next) {
  });
  //api
  //get all points, assuming standard identities
  router.get('/standard', function (req, res) {
    res.sendFile(path.join(app.get('staticPath'),'standard.csv'));;
    return;  
  })

  return router;
}

module.exports = api;