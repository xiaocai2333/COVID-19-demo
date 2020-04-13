# 文档说明
本文档主要介绍如何在本机部署demo。主要有以下几个步骤：
    
   首先要安装arctern，运行arctern要基于spark，先下载预编译的spark-3.0.0-preview2：
    
    wget https://mirror.bit.edu.cn/apache/spark/spark-3.0.0-preview2/spark-3.0.0-preview2-bin-hadoop2.7.tgz；
    
   其次，启动webservice服务端和客户端，目前部署webservice需要有arctern源码，需要通过源码才能启动webservice服务端和客户端。之后会将关于webservice的部分打包。
   arctern源码地址：
   
    https://github.com/zilliztech/arctern
    
   执行完上述操作之后就可以在webservice客户端进行画图。

### 具体安装arctern的方式参考以下链接：
    https://github.com/zilliztech/arctern-docs/blob/master/install_arctern_on_spark_en.md

### 启动webservice服务
   首先进入server目录下：
  ```shell script
    cd arctern/gui/server
  ```
   执行以下命令来启动服务：
  ```shell script
    python manage.py -r -p 8888 
  ```
   -r 表示启动服务， -p 表示端口（也可以不指定端口号，默认端口为8080，若指定了端口，在启动客户端时需要修改端口号与你指定的一致）

### 启动webservice客户端
   启动客户端时需要依赖nodejs，所以需要先安装nodejs，执行以下步骤以安装nodejs：
   ```shell script
      curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
      sudo apt-get install -y nodejs
      nodejs -v
   ```
   如果打印出版本号说明安装成功。
    
   修改gui/client/src/utils/Endpoints.ts文件，将ip和端口设置成本机的ip和上一步启动webservice时指定的端口。
   然后在gui/client/目录下执行
   ```shell script
      npm install
      npm start
   ```
   启动客户端之后会自动在浏览器中弹出网页，即webservice客户端可视化界面，也可以在浏览器中输入localhost:3000打开。
    
### 加载数据
加载数据之前先要创建数据表对应的json文件，需要指定数据表的schema和数据文件的路径，参考COVID-china-local.json文件。具体导入方式参考：
                        
    https://github.com/zilliztech/arctern/blob/master/gui/server/README.md

### 画图
   导入数据成功后就可以开始画图了，画图主要是以下几个步骤：     
   1. 在网页中打开localhost:3000，得到infini登录界面，输入用户名和密码进行登录（默认为zilliz和123456）
   2. 登录之后可以看到数据库配置界面，选择想要进行画图的数据库配置，点击保存配置
   3. 进入创建仪表盘界面，点击新建仪表盘，进入新增图表界面，点击新增图表
   4.进入画图界面，选择自己想要画图的类型，目前只支持点地图，选择点地图，在左边经纬度栏选择数据表中的经纬度列，就可以得到点地图了。