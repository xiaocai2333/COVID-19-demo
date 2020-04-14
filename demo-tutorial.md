# 文档说明
本文档主要介绍如何在本机部署demo。主要有以下几个步骤：
    
   首先要安装spark，下载[Arctern](https://github.com/zilliztech/arctern)，下载[infini-client](https://github.com/zilliztech/infini-client),
   
   其次启动webservice服务端和客户端，将数据导入到数据库中。
    
   执行完上述操作之后，可以在webservice客户端进行画图。

### 安装arctern：
   arctern的运行基于spark，首先下载并解压spark：
  ```shell script
    wget https://mirror.bit.edu.cn/apache/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz
    tar zxvf spark-3.0.0-preview2-bin-hadoop2.7.tgz
  ```
   arctern的安装参考以下链接：
   
    https://github.com/zilliztech/arctern-docs/blob/master/install_arctern_on_spark_en.md

### 启动webservice服务
   首先要下载json文件，在[db_json](./db_json)目录下。具体格式参照[COVID-china-local.json](./db_json/COVID-china-local.json)。下面展示了各个字段的意义（如要复制，请先删除注释）：
   ```json
{
    "db_name": "db2", //数据库name
    "type": "spark",  //基于spark运行
    "spark": {
        "app_name": "arctern",
        "master-addr": "local[*]",  //本地模式
        "PYSPARK_PYTHON": "/home/zc/miniconda3/envs/arctern/bin/python", //python路径
       "envs": {
        }
    },
    "tables": [   //数据表列表
        {
            "name": "local_china",
            "format": "csv",
            "path": "path/to/COVID-19-demo/data/COVID-china-data.csv", //数据路径
            "options": {
                "header": "True",
                "delimiter": ","
            },
            "schema": [ //数据表schema
                {"continent":  "string"},
                {"country": "string"},
                {"province": "string"},
                {"provinceLocationId": "long"},
                {"provinceCurrentConfirmedCount": "int"},
                {"provinceConfirmedCount": "int"},
                {"provinceSuspectedCount": "int"},
                {"provinceCuredCount": "int"},
                {"provinceDeadCount": "int"},
                {"cityName": "string"},
                {"longitude": "double"},
                {"latitude": "double"},
                {"cityLocationId": "long"},
                {"cityCurrentConfirmedCount": "int"},
                {"cityConfirmedCount": "int"},
                {"citySuspectedCount": "int"},
                {"cityCuredCount": "int"},
                {"cityDeadCount": "int"},
                {"updateTime": "string"}
            ],
            "visibility": "False" //前端是否可见
        },
        {
            "name": "china",
            "sql": "select longitude, latitude from local_china",
            "visibility": "True"
        }
    ]
}
```
   
   进入arctern/gui/server目录下,执行以下命令来启动服务：
  ```shell script
    python manage.py -r -c path/to/COVID-china-local.json
  ```
其中命令行参数说明如下：
```
-h help
-r production mode
-p http port
-i http ip
-c [path/to/data-config] load data
--logfile= [path/to/logfile], default: ./log.txt'
--loglevel= log level [debug/info/warn/error/fatal], default: info'
```
可以在启动服务时指定port（默认port是8080），若指定了port，在下一步启动客户端时需要修改port与你指定的一致。

如果想对数据库进行更多的操作（如查询等），请参考：
```
    https://github.com/zilliztech/arctern/blob/master/gui/server/README.md
```

### 启动webservice客户端
   启动客户端时需要依赖nodejs，所以需要先安装nodejs，执行以下步骤以安装nodejs：
   ```shell script
      curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
      sudo apt-get install -y nodejs
      nodejs -v
   ```
   如果打印出版本号说明安装成功。
   
   进入infini-client(前面有下载链接)，修改src/utils/Endpoints.ts文件，将ip和端口设置成本机的ip和上一步启动webservice时指定的端口(例子中是8888)。例如：
   ```
     let endpoint = `http://127.0.0.1:8888`;
   ```
   然后在infini-client目录下执行以下命令来启动客户端：
   ```shell script
      npm install
      npm start
   ```
   启动客户端之后会自动在浏览器中弹出网页，即webservice客户端可视化界面，也可以在浏览器中输入localhost:3000打开。

### 画图
   导入数据成功后就可以开始画图了，画图主要是以下几个步骤：     
   1. 在网页中打开localhost:3000，得到infini登录界面，输入用户名和密码进行登录（默认为zilliz和123456）
   2. 登录之后可以看到数据库配置界面，选择想要进行画图的数据库配置，点击保存配置
   3. 进入创建仪表盘界面，点击新建仪表盘，进入新增图表界面，点击新增图表
   4. 进入画图界面，选择自己想要画图的类型，目前只支持点地图，选择点地图，在左边经纬度栏选择数据表中的经纬度列，就可以得到点地图了。