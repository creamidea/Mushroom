蘑菇项目前端及其服务器开发环境
=======================

创建虚拟开发环境
------------
```shell
$ virtualenv --no-site-packages mushroom-env
```

进入开发环境
---------
```shell
$ mushroom-env\Scripts\django-admin.py mushroom
```

环境依赖导出
---------
```shell
(mushroom)$ pip freeze > product.dev
```

环境依赖导入
---------
```shell
(mushroom)$ pip install -r product.dev
```

安装django
---------
```shell
(mushroom)$ pip install django
```

### 创建工程
```shell
(mushroom)$ python mushroom-env\Scripts\django-admin.py startproject mushroom
```

=======
Mushroom
========
