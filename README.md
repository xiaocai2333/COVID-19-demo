# COVID-19-demo

（本文档中的端口8888只是一个例子，具体的按实际情况而定）
# 1.登录
curl -X POST -H "Content-Type: application/json" -d '{"username":"zilliz", "password":"123456"}' http://127.0.0.1:8080/login
# 2.将数据上传到hdfs

# 3.创建数据对应的json文件
    json文件中应包含数据的信息，例如数据路径，表信息，schema等(例如COVID-china.json)

与webservice交互有两种方式，但原理是一样的
一种是在Python中通过requests，另外一种是通过curl，以下以Python方式为例。
在微软晕上要先登录获取TOKEN，具体方法在arctern项目中都有
# 4.启动服务（微软云不需要自己手动起服务）
    python manage.py -r -p 8888 -c @./XXXX.json
    -r 表示启动服务， -p 表示端口， -c 表示在启动服务时就load数据到数据库中
    @./XXXX.json 表示你创建的json文件对应的路径
    
# 5.将数据load到数据库中
     可以在启动服务的时候直接将数据上传，若没有在启动服务时load数据，可以执行
     r=requests.post(url='http://localhost:8888/load', json=@./XXXX.json,headers={'Authorization': 'Token yourToken'} )

# 6.查询数据库
    r=requrests.get(url='http://localhost:8888/dbs', 'Token yourToken')

# 7.查询某数据库中的表信息
    r=requests.post(url='http://localhost:8888/db/table/info', 'Token yourToken')
    
# 8.画图
    画图之前要先写好sql语句的json
    r=requests.post(url='http://localhost:8888', 'Token yourToken', data=XXX.json)
   
登录 http://40.117.58.225:3000/login

1.选择自己的数据库
2.选择自己的数据表
3.选择画点地图，选择经纬度


