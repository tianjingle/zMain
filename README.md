# zMain
[个人学习]:整合baostack、tushare天天基金等数据源，筹码计算，多阶导数计算，k线绘制，智能选股和邮件提醒，机构调研数据获取等。

整合baostack、tushare天天基金等数据源，筹码计算，多阶导数计算，k线绘制，智能选股和邮件提醒，机构调研数据获取等。
- QQ：2695062879

![zMain效果图](src/NewTun/temp/sh.600059.png)

# 设置数据库的sql_model
```sql
set global sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

set session sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
```

# 添加机构调研的库
- 因为代码中没有判断机构调研的情况，因此这里手动的给添加上机构调研的库
```sql
use noun;
create table ajgdy (
 id varchar(64) not null primary key,
 CompanyCode text,
 CompanyName text,
 OrgCode text,
 OrgName text,
 OrgSum text,
 SCode text,
 SName text,
 NoticeDate text,
 StartDate text,
 EndDate text,
 Place text,
 Description text,
 Orgtype text,
 OrgtypeName text,
 Personnel text,
 Licostaff text,
 Maincontent text,
 ChangeP text,
 Close text);
```

# pip依赖的库
```sqlite
Package                       Version

----------------------------- ----------

-ip                           20.2.3
alabaster                     0.7.12
alembic                       1.4.3
altgraph                      0.17
asgiref                       3.3.1
Babel                         2.8.0
baostock                      0.8.8
beautifulsoup4                4.9.1
bs4                           0.0.1
certifi                       2019.11.28
chardet                       3.0.4
click                         7.1.2
colorama                      0.4.4
cycler                        0.10.0
Django                        3.1.4
django-basic-stats            0.2.0
docutils                      0.16
echarts-china-cities-pypkg    0.0.9
echarts-china-counties-pypkg  0.0.2
echarts-china-provinces-pypkg 0.0.3
echarts-countries-pypkg       0.1.6
fire                          0.3.1
Flask                         1.1.2
flask-marshmallow             0.9.0
Flask-Migrate                 2.3.0
Flask-SQLAlchemy              2.1
future                        0.18.2
icon-font-to-png              0.4.1
idna                          2.8
imageio                       2.9.0
imagesize                     1.2.0
itsdangerous                  1.1.0
jiagu                         0.2.3
jieba                         0.42.1
Jinja2                        2.11.1
kiwisolver                    1.2.0
lml                           0.0.2
lxml                          4.5.1
Mako                          1.1.3
MarkupSafe                    1.1.1
marshmallow                   2.13.6
matplotlib                    3.2.1
mpl-finance                   0.10.1
mplfinance                    0.12.7a0
numpy                         1.18.4
packaging                     20.4
palettable                    3.3.0
panda                         0.3.1
pandas                        1.0.4
pefile                        2019.4.18
Pillow                        8.0.1
pip                           19.0.3
prettytable                   0.7.2
pyecharts                     1.7.0
pyecharts-jupyter-installer   0.0.3
Pygments                      2.7.2
pyinstaller                   4.2.dev0
pyinstaller-hooks-contrib     2020.10
PyMySQL                       0.10.1
pyparsing                     2.4.7
pystache                      0.5.4
python-dateutil               2.8.1
python-editor                 1.0.4
python-nmap                   0.6.1
python3-nmap                  1.4.8
pytils                        0.3
pytz                          2020.1
pywin32-ctypes                0.2.0
requests                      2.22.0
scapy                         2.4.4
scipy                         1.5.3
selenium                      3.141.0
setuptools                    41.2.0
simplejson                    3.17.0
six                           1.14.0
snowballstemmer               2.0.0
soupsieve                     2.0.1
Sphinx                        3.3.0
sphinx-rtd-theme              0.5.0
sphinxcontrib-applehelp       1.0.2
sphinxcontrib-devhelp         1.0.2
sphinxcontrib-htmlhelp        1.0.3
sphinxcontrib-jsmath          1.0.1
sphinxcontrib-qthelp          1.0.3
sphinxcontrib-serializinghtml 1.1.4
splinter                      0.14.0
SQLAlchemy                    1.2.13
sqlparse                      0.4.1
static                        1.1.1
stylecloud                    0.5.1
TA-Lib                        0.4.19
tablib                        2.0.0
termcolor                     1.1.0
tinycss                       0.4
tools                         0.1.9
tushare                       1.2.60
urllib3                       1.25.7
websocket-client              0.57.0
Werkzeug                      1.0.1
wordcloud                     1.8.1

```




# 安装ta-lib的方法
1. ta-lib不能直接用pip install ta-lib的方式进行安装，需要下载whl文件，然后pip install xxx.whl的方式进行安装
2. 确认自己的python的版本，比如我本地安装的是python3.8
3. 去[python第三方库](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)中下载和我们python匹配的ta-lib，因为我们的python是3.8，操作系统是64，所以我们下载cp38,64位
4. 使用管理员权限运行cmd，执行命令：pip install "C:\Users\Administrator\Downloads\TA_Lib-0.4.20-cp38-cp38-win_amd64.whl"
5. 安装完成

# git 提交代码设置postbuffer大小
```sqlite
git pull
git add .
git commit -m '123'
git pull
git config http.postBuffer 524288000
git push
```

