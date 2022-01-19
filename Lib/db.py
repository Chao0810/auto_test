import pymysql,logging  #导入pymysql包
from Config import config

#建立数据库连接
class DB():
    def __init__(self):
         self.conn = pymysql.connect(
                host = config.Host,
                port = config.Port,
                user = config.User,
                passwd =config.Passwd,
                db = config.Db,
                charset = config.Charset
            )
         self.cur =self.conn.cursor()

    def __del__(self): #析构函数，实例删除时触发
        self.cur.close()
        self.conn.close()

     #数据库查询操作(查)
    def select_db(self,sql):
        self.cur.execute(sql)   #执行sql
        result = self.cur.fetchall() #获取所有查询结果
        return result

    #数据库更改操作（改）
    def updata_db(self,sql):
        try:
             self.cur.execute(sql)   #执行sql
             self.conn.commit() #提交更改
             return True
        except Exception as e:
            self.conn.rollback() #回滚操作
            logging.info(e)
            return False

    #数据库检查数据操作
    def check_db(self,tab,key,value):
         result = self.select_db("select * from {} where {} = '{}'".format(tab,key,value)) #系统把字符串value当做了mysql的关键字,因此需要单引号引起来
         return True if result else False

    #数据库删除数据操作
    def del_db(self,tab,key,value):
         result = self.updata_db("delete from {} where {} = '{}'".format(tab,key,value))
         return True if result else False

if __name__ == "__main__":
    Db = DB()
    if Db.check_db(tab="user",key="account",value="hc2") == True:#json.loads(data)["account"]
    #re = Db.del_db(tab="user",key="account",value="hc2")
       print("success")
