var express = require('express');
var router = express.Router();

var Database = require('./mySQL_connect');
/* GET users listing. */
router.get('/', function(req, res, next) {
    new Database().getLatest(res,req);
});
router.post('/',function (req, res, next) {
    new Database().updateLevel(res,req);
});
module.exports = router;
