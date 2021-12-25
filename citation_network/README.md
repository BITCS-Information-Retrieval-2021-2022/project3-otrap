# 后端运行方法(citation_network)

安装anaconda并创建虚拟环境（Python==3.6），激活虚拟环境
Install the dependencies
```bash
conda install
django==2.2.6
drf-haystack==1.8.11
elasticsearch==5.5.3
djangorestframework==3.12.4
elasticsearch-dsl==5.3.0
```
配置mongodb和elasticsearch，参考：https://www.yuque.com/huajian-z02yc/ycr4n1/az0epz

导入MongoDB数据,期间请打开Mongo-connector服务，
在cmd中输入
```bash
mongorestore -h 127.0.0.1 -d otrap D:\otrap
```
-h后为MongoDB的一个地址，otrap为要导入的数据库名称，D:\otrap为数据存放位置




### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
python manage.py runserver
```
