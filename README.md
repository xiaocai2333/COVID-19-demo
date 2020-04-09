# COVID-19-demo

通过Python与webservice交互
（本文档中的端口8888只是一个例子，具体的按实际情况而定）
# 1.登录
    response = requests.post(url='http://microsoft1:8888/login', json={"username": "zilliz", "password": "123456"})
    通过登录可以得到token
    Token = respond.json()['data']['token']
    headers={'Content-Type': 'application/json', 'Authorization': 'Token %s' %Token}
# 2.将数据上传到hdfs
    hdfs dfs -put *.csv /data(选择想要上传的文件进行上传)

# 3.创建数据表对应的json文件
    json文件中应包含数据的信息，例如数据路径，表信息，schema等(例如COVID-china.json)

# 4.启动服务（微软云不需要自己手动起服务）
    python manage.py -r -p 8888 -c @./XXXX.json
    -r 表示启动服务， -p 表示端口， -c 表示在启动服务时就load数据到数据库中
    @./XXXX.json 表示你创建的json文件对应的路径
    
# 5.将数据load到数据库中
     可以在启动服务的时候直接将数据上传，若没有在启动服务时load数据，可以执行
     r=requests.post(url='http://localhost:8888/load', json=@./XXXX.json,headers=headers)
     XXXX.json是要构造的数据表对应的json文件,在Python中可以先读取json文件的内容，json=读取的内容
     
# 6.查询数据库
    r=requrests.get(url='http://localhost:8888/dbs', headers=headers)
    （这里的方法是get）
# 7.查询某数据库中的所有表
    r=requests.post(url='http://localhost:8888/db/tables', json={'id': 'database_id'}, headers=headers)
    
# 8.查询某数据库中的表信息
    r=requests.post(url='http://localhost:8888/db/table/info', json=@./XXXX.json, headers=headers)
    这里的XXX.json文件表示数据表信息，例如：
```json
{
    "id": "database_id",
    "table": "table_name"
}
```
    也可以直接写到代码中
    
# 9.query查询
    r=requests.post(url='http://localhost:8888/db/query', headers=headers, data=@./XXX.json)
# 10.画点图
    画图之前要先写好sql语句的json
    r=requests.post(url='http://localhost:8888', headers=headers, data=@./XXX.json)
   
登录 http://40.117.58.225:3000/login

1.选择自己的数据库
2.选择自己的数据表
3.选择画点地图，选择经纬度


