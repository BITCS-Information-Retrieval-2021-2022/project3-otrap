# 后端部署、启动运行流程(citation_network)（篇幅限制的都写了"参考"）

安装anaconda并创建虚拟环境（Python==3.6），激活虚拟环境
Install the dependencies
```bash
conda install
django==2.2.6
elasticsearch==5.5.3
elasticsearch-dsl==5.3.0
```
配置mongodb和elasticsearch，参考：https://www.yuque.com/huajian-z02yc/ycr4n1/az0epz

打开mongo-connector服务，导入MongoDB数据：
在cmd中输入
```bash
mongorestore -h 127.0.0.1 -d otrap D:\otrap
```
-h后为MongoDB的一个地址，otrap为要导入的数据库名称，D:\otrap为数据存放位置

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
python manage.py runserver
```

# 代码说明（篇幅限制的都写了"参考"）
代码目录结构说明，参考：https://blog.csdn.net/Xiayuyuren_Study/article/details/85127905 

代码必要说明：见代码注释
