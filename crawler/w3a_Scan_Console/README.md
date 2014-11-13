w3a_scan_console 是什么？
=========================

    W3A SCAN 是一个新开启的项目，基于Python作为底层语言做的Web扫描器。
预备实现的功能涵盖以下功能：

- Web Sprider (页面爬虫) -----------------------------------------[Ok][100%]
- Web Page (Form/AJAX) distinguish (页面(表单|ajax)识别) ---------[OK][100%]
- Nmap Scanning (Nmap扫描模块) -----------------------------------[Ok][100%]
- Web Directory probe (目录探测) ---------------------------------[Filed][50%]
- Web Cross-Site script probe (跨站脚本探测) ---------------------[Filed][0%]
- Web Sql inject probe (SQL注入探测) -----------------------------[Filed][0%]
- Web Fingerprint (指纹识别) -------------------------------------[Filed][0%]
- Web LFI/RFI file contains(远程/本地文件包含) -------------------[Filed][0%]
- Follow-up update..... (后续更新...)


Structure(结构)
=======================
- ├── conf  [配置文件目录]
- │   └── db.ini [数据库配置]
- ├── dic [字典配置]
- │   └── dictionary.dic [目录字典]
- ├── lib [公共库]
- │   ├── DB_module.py
- │   ├── __init__.py
- │   ├── __init__.pyc
- │   ├── log_exec.py
- │   └── log_exec.pyc
- ├── LICENSE
- ├── log [日志管理]
- │   ├── module [模块错误日志]
- │   └── sys  [主程序错误日志]
- │       └── f461c96407e745f44f3ae750787e19b6.log
- ├── main.py [主程序]
- ├── image [图片展示]
- ├── db_script [数据库脚本]
- ├── module [待改写的模块]
- │   ├── db_module.py
- │   ├── directory-test_module.py
- │   ├── form-test_module.py
- │   ├── nmap_module.py
- │   └── sprider_module.py
- ├── plugin [插件位置]
- │   ├── DirectioryScan.py
- │   ├── DirectioryScan.pyc
- │   ├── __init__.py
- │   ├── __init__.pyc
- │   ├── SQLinjectScan.py
- │   └── SQLinjectScan.pyc
- └── README.md

Help (帮助)
========================
   前期编写的都是以模块的形式出现，后期当框架建立起来以后，将会扫瞄的模块将会以
插件的形式出现。目前的想法主要是想将一些常见的功能实现出来，待后续需求确定以后再
对整个扫瞄的架构进行调整。
	所有的更新日志以及W3A SCAN开发进度，且看以下地址：
	link: https://github.com/smarttang/w3a_Scan_Console/wiki/_pages


Readme (说明)
========================
  - 1) 该项目会长期维护，后续会有web界面.(W3a Scan)
  - 2) 该项目更新的方式主要是以git更新的方式为准
  - 3) 模块的进度意义：</br>
      --10% 构思完成</br>
      --20% 代码正在编写</br>
      --30%-50% 代码正在更新,细节正在重写</br>
      --60%-80% 代码正在测试,修复bug和测试模块是否可用</br>
      --90% 校正bug,留下使用例子,确定插入sql结构</br>
      --100% 基本功能实现完成</br>

Exec Demo(执行Demo)(2014-1-23)
=======================
<img style="max-width:100%;" title="Run example" alt="Run example" src="https://raw2.github.com/smarttang/w3a_Scan_Console/master/image/demo1.png">

FindMe (找我)
=======================
  - Name: Smart
  - QQ:505575655
  - Email: tangyucong@163.com
