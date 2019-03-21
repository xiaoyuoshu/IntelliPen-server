var mysql = require('mysql');

class Database{
    constructor(){
        this.connection = mysql.createConnection({
            host:'localhost',
            user: 'root',
            password:'xiaoyuoshu',
            database: 'IntelliPen',
            port:3306
        });
    }
    formSubmit(res,req){
        console.log('req:\n'+req);
        var that = this
        var dataList = req.body
        this.connection.query('select *, count(distinct collectTime) from res where type = "斜钩：㇂" group by collectTime',
            //select *, count(distinct name) from table group by name
            function (err,result) {
                if(err){
                    console.log(err);
                }
                else{
                    console.log(result)
                    var group_len = 1
                    if(result != null) {
                        group_len = result.length + 1
                    }
                    console.log('group_len:' + group_len)
                    console.log('result:' + result)
                    for(var i = 0;i < dataList.length;i++) {
                        that.connection.query('insert into res set ?', {
                            collectTime: dataList[i].collectTime,
                            currentTime: dataList[i].currentTime,
                            w_alpha: dataList[i].w_alpha,
                            w_beta: dataList[i].w_beta,
                            w_gama: dataList[i].w_gama,
                            a_x: dataList[i].a_x,
                            a_y: dataList[i].a_y,
                            a_z: dataList[i].a_z,
                            alpha: dataList[i].alpha,
                            beta: dataList[i].beta,
                            gama: dataList[i].gama,
                            force1: dataList[i].force1,
                            force2: dataList[i].force2,
                            force3: dataList[i].force3,
                            type: dataList[i].type,
                            level: dataList[i].level,
                            groups: group_len,
                        }, function (err, result) {
                            if (err) {
                                console.log(err);
                            }
                        });
                    }
                    res.send('ojbk')
                }
            })
    }
    down(res,req){
        var timenow = (Date.now() - 1)
        this.connection.query('select * from res into outfile ' + '\'/tmp/' + timenow + 'ipen.csv\'' + 'fields terminated by \',\' optionally enclosed by \'"\' escaped by \'"\'    lines terminated by \'/r/n\'',
            function (err,result) {
                if(err){
                    console.log(err);
                }
                else{
                    console.log('\'/tmp/' + timenow + 'ipen.csv\'');
                    res.download('/tmp/',timenow + 'ipen.csv');
                }
            })
    }
    getLatest(res,req){
        this.connection.query('select * from res where currentTime=(select max(currentTime) from res)',
            function (err,result) {
                if(err){
                    console.log(err);
                } else {
                        res.send(result)
                }
            })
    }
    getGroups(res,req){
        this.connection.query('select *, count(distinct groups) from res group by groups',
            function (err,result) {
                if(err){
                    console.log(err);
                } else {
                    res.send(result)
                }
            })
    }
    initGroups(res,req){
        console.log(req.body)
        this.connection.query('select *, count(distinct collectTime) from res where groups='+req.body.id+' group by collectTime',
            function (err,result) {
                if(err){
                    console.log(err);
                } else {
                    res.send(result)
                }
            })
    }
    updateLevel(res,req){
        console.log(req.body)
        this.connection.query('update res set level='+req.body.newlevel+' where groups='+req.body.groups+' and type=\"'+req.body.strock+'\"',
            function (err,result) {
                if(err){
                    console.log(err);
                } else {
                    res.send('ojbk')
                }
            })
    }
}
module.exports = Database;
