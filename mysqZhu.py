import pymysql
import re
import threading
lock = threading.Lock()
class MysqlZhu:
    """
        auther:zhu
        类用于连接mysql数据库
        类创建即连接
        类消失即关闭数据库
    """

    def __init__(self,host='localhost',port = 3306,database="qnh",
                                user='root',password='',charset='utf8'):
        """
        初始化方法
        """    
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset
        self.__cursor = None
        self.__connect = None
        self.__get_mysql_cursor()
    def __del__(self):
        self.__close()
    def __get_mysql_cursor(self):
        """
        创建对象后直接获取游标即可使用
        """
        data_dict = {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password,
            "charset": self.charset
        }
        # 连接数据库
        try:
            self.__connect = pymysql.connect(**data_dict)
            self.__cursor = self.__connect.cursor()
        except Exception as ex:
            # print("-----------Host:%s Database:%s User:%s error！！-----------提示："%(self.host,self.database,self.user),ex)
            self.__cursor = None
        else:
            pass
            # print("-----------Host:%s Database:%s 用户:%s success！！-----------"%(self.host,self.database,self.user))

    # 执行sql语句
    def execute_sql(self, sql,*args):
        # 查询语句
        if not self.__cursor:
            return False
        sql_del_pace = re.sub(' +','',sql,count=1)
        # pace1 = sql.replace(" ","")
        # print(sql_del_pace)
        re_result = re.match("[^ ]*", sql_del_pace, re.I).group()
        
        if re_result.lower()[:6] == "select":
            lock.acquire()
            self.__cursor.execute(sql,args=args)
            lock.release()
            # print("-----------Host:%s Database:%s User:%s action:%s param：%s Complete！-----------"%(self.host,self.database,self.user,sql,args))
            return self.__cursor.fetchall()
        else:
            # 执行更新、插入、修改语句
            lock.acquire()
            self.__cursor.execute(sql,args=args)
            self.__connect.commit()
            lock.release()
            # print("-----------Host:%s Database:%s User:%s action:%s param：%s Complete！-----------"%(self.host,self.database,self.user,sql,args))
            return self.__cursor.lastrowid
        
        
                     
    def __close(self):
        """
        关闭数据库连接
        """
        self.__cursor.close()
        self.__connect.close()
        # print("-----------Host:%s Database:%s User:%s The database is down！！-----------"%(self.host,self.database,self.user))
        # print("-----------The database is down!-----------")
