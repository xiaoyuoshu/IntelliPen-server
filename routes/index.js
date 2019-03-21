var express = require('express');
var Database = require('./mySQL_connect');
var router = express.Router();

/* GET home page. */
router.get('/:name', function(req, res, next) {
    console.log(req.params.name)
    res.sendFile('/www/IntelliPenService/routes/'+req.params.name+'.png')
});

router.post('/submit',function (req, res, next) {
    console.log(req.body);
    new Database().formSubmit(res,req);
});


module.exports = router;
