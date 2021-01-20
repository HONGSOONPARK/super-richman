module.exports = router;

var express = require('express');
var mysql_dbc = require('../config/database')();
var connection = mysql_dbc.init();
var router = express.Router();

mysql_dbc.test_open(connection);


/* GET home page. */
router.get('/', function(req, res, next) {
  var params = '';
  var sql1 = `SELECT NO, NAME, AMOUNT, PER, PRICE, DIFF, FLUC FROM tiger ORDER BY NO ASC`;

  connection.query(sql1, function (error, results, fields){
    if (!error) {
      console.log('first');
      console.log(results);
      res.render('index', {list: results});


    }else{
      console.log('query error : ' + error);
    }
  });
  

});

module.exports = router;