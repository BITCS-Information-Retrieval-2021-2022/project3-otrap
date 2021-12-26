# Proj3-otrap

## 项目要求
1.使用大规模数据处理技术构建引文网络来计算论文重要性分数  
2.搭建Elasticsearch实现从某一个或若干字段检索  
3.结合引文网络重要性分数对检索结果进行调整  
4.当选中一篇论文后，能够以该节点为中心展示引文网络子图  
5.设计并实现一个学术论文搜索引擎网站

## 任务点与分工
1.处理算法(类PageRank)：茅晓璐、李和松  
2.Grape构建引文网络及图计算：茅晓璐  
3.MongoDB：鲍志浩、梁华健  
数据库创建、存储、维护  
4.Elasticsearch：梁华健  
（1）创建索引  
（2）检索逻辑 结合引文网络重要性分数  
5. 后端：梁华健、严畅  
6. 前端：张琦  
7. 可视化模块：张琦

## 开发工具
1.图计算框架：grape  
2.数据库：MongoDB  
3.检索：ElasticSearch   
4.后端：Python、Django  
5.前端：QUASAR、vue2 vuex vue-router、axios、RESTful

## 项目结构

![Image text](https://github.com/BITCS-Information-Retrieval-2021-2022/project3-otrap/blob/main/images/后端.png)

## 代码风格

![Image text](https://github.com/BITCS-Information-Retrieval-2021-2022/project3-otrap/blob/main/images/flake8.jpg)

## 后端部署、启动运行流程(citation_network)（`篇幅限制的都写了"参考"`）

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

# 代码说明（`篇幅限制的都写了"参考"`）
代码目录结构说明，参考：https://blog.csdn.net/Xiayuyuren_Study/article/details/85127905 

代码必要说明：见代码注释



## 前端运行方法(frontend-proj3)
安装 node.js，详见：[安装教程](https://zhuanlan.zhihu.com/p/82347262)

安装 Quasar CLI，详见：http://www.quasarchs.com/quasar-cli/installation#introduction


# 代码说明（`篇幅限制的都写了"详见参考"`）
代码目录结构说明：

详见：http://www.quasarchs.com/quasar-cli/directory-structure#introduction

代码必要说明：

见代码注释

部署过程、启动运行流程：


**Install the dependencies**
```bash
npm install
```

**Start the app in development mode (hot-code reloading, error reporting, etc.)**
```bash
quasar dev
```

依赖的第三方库的目录及版本：
```json
{
  "name": "frontend-proj3",
  "author": "otrap",
  "scripts": {
    "lint": "eslint --ext .js,.vue ./",
    "test": "echo \"No test specified\" && exit 0"
  },
  "dependencies": {
    "@quasar/extras": "^1.0.0",
    "axios": "^0.21.1",
    "core-js": "^3.6.5",
    "echarts": "^5.2.2",
    "quasar": "^1.0.0"
  },
  "devDependencies": {
    "@quasar/app": "^2.0.0",
    "babel-eslint": "^10.0.1",
    "eslint": "^7.21.0",
    "eslint-config-prettier": "^8.1.0",
    "eslint-plugin-vue": "^7.7.0",
    "eslint-webpack-plugin": "^2.4.0"
  },
  "browserslist": [
    "last 10 Chrome versions",
    "last 10 Firefox versions",
    "last 4 Edge versions",
    "last 7 Safari versions",
    "last 8 Android versions",
    "last 8 ChromeAndroid versions",
    "last 8 FirefoxAndroid versions",
    "last 10 iOS versions",
    "last 5 Opera versions"
  ],
  "engines": {
    "node": ">= 10.18.1",
    "npm": ">= 6.13.4",
    "yarn": ">= 1.21.1"
  }
}

```
