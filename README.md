The MIT License (MIT)
[OSI Approved License]
The MIT License (MIT)

Copyright (c) 2013 August Trek (creamidea@gmail.com), macc(497066099@qq.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

蘑菇项目前端及其服务器开发环境
=======================

虚拟开发环境
------------

**创建**
```shell
$ virtualenv --no-site-packages mushroom-env
```

**进入**
```shell
$ mushroom-env\Scripts\django-admin.py mushroom
```

**环境依赖导出**
```shell
(mushroom)$ pip freeze > product.dev
```

**环境依赖导入**
```shell
(mushroom)$ pip install -r product.dev
```

**安装django**
```shell
(mushroom)$ pip install django-pipeline
```

**安装和配置django-pipeline**
安装
```shell
(mushroom)$ pip install django-pipeline
```

配置:

暂时提供windows平台的配置，请参考[这里](https://github.com/creamidea/Mushroom/issues/10)
（我想应该没有什么比在Windows上配置环境更加的难过的事情了吧（笑））

Reference:
[Installation](http://django-pipeline.readthedocs.org/en/latest/installation.html)

**创建工程**
```shell
(mushroom)$ python mushroom-env\Scripts\django-admin.py startproject mushroom
```

===========
文件夹结构目录
===========

```
| - Document 生成的文档以及参考的文档
  | - Sphinx生成的文档
  | - 表现层设计文档
| - NodeSite Django工程所在目录
  | - NodeSite Django代码所在目录
  | - static 静态文件所在目录，使用python manage.py collectstatic导入到目录
| - UIDesign UI界面设计
| - Vendor   库提供商
```

========
Mushroom
========

=====
ISSUE
=====
用于记录django开发过程中遇到的问题，或者学习到的相关新知识，或者好的点子
地址：https://github.com/creamidea/Mushroom/issues
