var express = require('express');
var router = express.Router();
var Database = require('./mySQL_connect');
var fs = require("fs");
var exec = require('child_process').exec;

/* GET users listing. */
router.post('/', function(req, res, next) {
    var tempString = "\"collectTime\",\"currentTime\",\"a_x\",\"a_y\",\"a_z\",\"alpha\",\"beta\",\"gama\",\"w_alpha\",\"w_beta\",\"w_gama\",\"force1\",\"force2\",\"force3\",\"type\",\"level\",\"groups\"\n"
    for(var i = 0;i < req.body.Data.length;i++){
        tempString += ("\"" + req.body.Data[i].collectTime + "\","
                + "\"" + req.body.Data[i].currentTime + "\","
                + "\"" + req.body.Data[i].a_x + "\","
                + "\"" + req.body.Data[i].a_y + "\","
                + "\"" + req.body.Data[i].a_z + "\","
                + "\"" + req.body.Data[i].alpha + "\","
                + "\"" + req.body.Data[i].beta + "\","
                + "\"" + req.body.Data[i].gama + "\","
                + "\"" + req.body.Data[i].w_alpha + "\","
                + "\"" + req.body.Data[i].w_beta + "\","
                + "\"" + req.body.Data[i].w_gama + "\","
                + "\"" + req.body.Data[i].force1 + "\","
                + "\"" + req.body.Data[i].force2 + "\","
                + "\"" + req.body.Data[i].force3 + "\","
                + "\"" + req.body.Data[i].type + "\","
                + "\"" + "1" + "\","
                + "\"" + "1" + "\"\n")
    }
    fs.writeFile('/www/IntelliPenService/routes/input.csv', tempString,  function(err) {
        if (err) {
            return console.error(err);
        }
        exec('python /www/IntelliPenService/routes/API.py '+ req.body.TYPE.toString()+' '+'/www/IntelliPenService/routes/input.csv'+' ',function(error,stdout,stderr){
            console.log('you level',stdout);
            if(error) {
                console.info('stderr : '+stderr);
            }
            res.send(stdout)
        });
    });
});

module.exports = router;
