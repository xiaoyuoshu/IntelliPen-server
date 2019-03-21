# IntelliPenServer

力度矫正笔--服务器端

### 架构

1. 语言：JavaScript（ECS6）
2. 实际运行环境：Node.js（V8.9.0）
3. 实际系统环境：CentOs 7.4
4. 操作数据库：mysql 5.1

### 文件目录与文件含义
```
bin
  └─www //可执行文件，使用端口号为'3000'
node_modules //存放 package.json 中安装的模块
public //存放公共资源文件（未使用）
routes //路由控制文件
  ├─download.js //转发getGroups()和initGroups()需求
  ├─users.js //转发getLatest()和updateLevel()需求
  ├─index.js //转发formSubmit()需求
  ├─getLevel.js //获取用户数据并分析，然后返回结果
  ├─mySQL_connect.js //连接mysql数据库，以及处理各类数据库增删查改操作
  ├─API.py //机器学习分析脚本
  ├─input.csv //用户的笔画数据缓存，供API.py分析
  ├─aveList_*.npy //标准力度数据保存文件
  ├─*.png //用户笔画力度与标准力度数据的对比图表
  └─model*.pkl //模型保存文件
views //存放html模板文件（未使用）
app.js //项目入口文件
package.json //存储工程的信息及模块依赖
```

### 路由处理

#### GET请求

1. '/users'

   调用Database().getLatest(res,req)方法

   查询数据库中最近的一条笔画记录

2. '/download'

   调用Database().getGroups(res,req)方法

   获取数据库中笔画的分组情况

3. '/image/*'

   获取第*个力度对比图片

#### POST请求

1. '/index'

   调用Database().getGroups(res,req)方法

   将一组训练用数据存储进入数据库

2. '/users'

   调用Database().updateLevel(res,req)方法

   用于重判数据等级时，将对应分组中的对应笔画的等级更新

3. '/download'

   调用Database().initGroups(res,req)方法

   查询对应组号中的所有笔画数据

4. '/getLevel'

   将上传的一组笔画数据存储进入input.csv中，调用API.py获取笔画数据对应的等级，并返回给用户

### 数据库结构

数据库名：IntelliPen

表名：res

| 名字        | 类型       | 含义                   |
| ----------- | ---------- | ---------------------- |
| collectTime | bigint(20) | 一组笔画开始收集的时间 |
| currentTime | bigint(20) | 笔画数据点当前的时间   |
| a_x         | int(11)    | x轴方向加速度          |
| a_y         | int(11)    | y轴方向加速度          |
| a_z         | int(11)    | z轴方向加速度          |
| alpha       | double     | 角度α                  |
| beta        | double     | 角度β                  |
| gama        | double     | 角度γ                  |
| w_alpha     | int(11)    | 角速度α                |
| w_beta      | int(11)    | 角速度β                |
| w_gama      | int(11)    | 角速度γ                |
| force1      | int(11)    | 力度1                  |
| force1      | int(11)    | 力度2                  |
| force1      | int(11)    | 力度3                  |
| type        | text       | 笔画种类               |
| level       | text       | 笔画判定等级           |
| groups      | int(11)    | 笔画所在大组组号       |

