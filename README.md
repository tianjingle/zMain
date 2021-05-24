# zMain
[个人学习]:整合baostack、tushare天天基金等数据源，筹码计算，多阶导数计算，k线绘制，智能选股和邮件提醒，机构调研数据获取等。

整合baostack、tushare天天基金等数据源，筹码计算，多阶导数计算，k线绘制，智能选股和邮件提醒，机构调研数据获取等。

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
