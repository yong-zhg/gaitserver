#注册 signup
{
        "user" : {
                 "name" : "1",
                 "password" : "1",
                 "real_name" : "1",
                 "height" : 172,
                 "weight" : 60,
                 "sex" : 1,
                 "birthday" : "1994-10-1",
                 "email" : "123456@qq.com"
         }
}
{
        "user" : {
                 "name" : "2",
                 "password" : "2",
                 "real_name" : "2",
                 "height" : 172,
                 "weight" : 60,
                 "sex" : 1,
                 "birthday" : "1994-10-2",
                 "email" : "123457@qq.com"
         }
}

#登陆 login
{
    "user":{
        "name":"1",
        "password":"1"
    }
}
#logout
{
    "token": "rMdXkUeiA8fTysCju2GlaVg4cSxW5t"#查看数据库获取token
}

#subscribe
{
    "token":"rMdXkUeiA8fTysCju2GlaVg4cSxW5t",
    "user" :{
        "name":"2"
    }
}

#info
{
    "token": "rMdXkUeiA8fTysCju2GlaVg4cSxW5t"
}

#info/update
{
    "token": "rMdXkUeiA8fTysCju2GlaVg4cSxW5t",
    "user": {
        "name": "1",
        "real_name": "1_1",
        "height": 173,
        "weight": 61,
        "sex": 0,
        "birthday": "1994-9-1",
        "email": "123451@qq.com"
    }
}

#password/update
{
    "token":"rMdXkUeiA8fTysCju2GlaVg4cSxW5t",
    "user":{
        "name":"1",
        "old_password": "1",
        "new_password": "11"
    }
}
{
    "token":"rMdXkUeiA8fTysCju2GlaVg4cSxW5t",
    "user":{
        "name":"1",
        "old_password": "11",
        "new_password": "1"
    }
}

#data/upload
{
    "token":"rMdXkUeiA8fTysCju2GlaVg4cSxW5t",
    "timestamp": "1",
    "device_id": "1",
    "data": {
          "signal":[
                {
                      "signal_strength": 1,
                      "timestamp": 1
                }
           ],
          "pressure":[
                {
                      "timestamp": 1,
                      "a":1,
                      "b":2,
                      "c":3,
                      "d":4
                },
                {
                       "timestamp": 1,
                       "a":5,
                       "b":6,
                       "c":7,
                       "d":8
                }
          ],
          "acceleration":[
               {
                       "timestamp": 1,
                       "x":1,
                       "y":2,
                       "z":3
               },
               {
                       "timestamp": 1,
                       "x":4,
                       "y":5,
                       "z":6
               }
          ],
          "angleAcceleration":[
               {
                       "timestamp": 1,
                       "x":1,
                       "y":2,
                       "z":3
               },
               {
                       "timestamp": 1,
                       "x":4,
                       "y":5,
                       "z":6
               }
          ],
    }
}




#data/query
{
    "token":"rMdXkUeiA8fTysCju2GlaVg4cSxW5t",
    "user":{
          "name":"1"
    },
    "type":[
           "int",
           "double",
           "string"
    ],
    "filter":{
           
    }
}

# data/pressures/query
# data/acceleration/query
# data/angleacceleration/query
# data/signal/query
{
      "filter":{
              "start_time":1,
              "end_time": 1
      }
}






















