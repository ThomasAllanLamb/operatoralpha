var express = require('express');
var path = require('path');

//???: is there a less confusing way to name this?
function api (app) {
  var router = express.Router();

  //main page displays a demo of the api
  router.get('/', function(req, res, next) {
  });
  //api
  //get all points, assuming standard identities
  router.get('/standard', function (req, res) {
    res.sendFile(path.join(app.get('dataPath'),'standard.csv'));;
    return;  
  })

  return router;
}

module.exports = api;