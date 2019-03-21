var express = require('express');
var router = express.Router();
var Database = require('./mySQL_connect');

/* GET users listing. */
router.get('/', function(req, res, next) {
    new Database().getGroups(res,req);
});

router.post('/',function (req, res, next) {
    new Database().initGroups(res,req);
});
module.exports = router;
