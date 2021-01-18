# mysqlZhu
### python 连接 MySql 简化连接程序。 
#### 执行SQL只需要两步 
```python
1. 第一步：
mysqlZhu = MysqlZhu(host='主机名',port = 3306,database="数据库",user='数据库用户名',password='数据库密码',charset='utf8') 
2. 第二步：
# 如果是插入这返回插入后的下标，如果是查询，返回的是列表，如果是是修改直接修改即可
result = mysqlZhu.execute_sql("您的SQL语句")
```
