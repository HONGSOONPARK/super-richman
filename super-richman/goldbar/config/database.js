var mysql = require('mysql');

module.exports = function () {
  return {
    init: function () {
      return mysql.createConnection({
        host: '125.242.169.153',
        port: '3306',
        user: 'richman',
        password: 'richman',
        database: 'richman',
        multipleStatements: true
      })
    },
    
    test_open: function (con) {
      con.connect(function (err) {
        if (err) {
          console.error('mysql connection error :' + err);
        } else {
          console.info('mysql is connected successfully.');
        }
      })
    }
  }
};
