# 后端运行方法(citation_network)

## Choice A:
安装anaconda并创建虚拟环境，激活虚拟环境
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




### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
python manage.py runserver
```
## Choice B: 
```bash
open the app with pycharm,  
1.set "Run browser":http://127.0.0.1:8000/   
                           2.Python interpreter 3.6(project3-otrap)  
3.Click "Fix"(if exist)  
4.Setiings→Languages&Frameworks→Django→Enable Django Support   
5.run otrap
```
