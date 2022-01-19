#配置Log的相关信息
import logging,os,time


#连接数据库的信息
Host = "192.168.107.135"
Port = 3306
User = "root"
Passwd = "admin" #数据库的密码
Db = "fresho2o"
Charset = "utf8"

#各个sheet页的名字
sh1 = "Login"
sh2 = "Register"
sh3 = "queryReceiveAddr"
sh4 = "addReceiveAddr"
sh5 = "selectGoodCategory"
sh6 = "addOrder"
sh7 = "selectOrder"
sh8 = "unfinishOrder"
sh9 = "finishOrder"


#发送邮件的相关配置
smtp_server = "smtp.qq.com"
smtp_port = 465
smtp_user = "2510704230@qq.com"
smtp_password = "joxcjoscinssdihd"

sender = smtp_user #发件人
receiver = ["2510704230@qq.com"] #["2510704230@qq.com","2637188236@qq.com"] #收件人,以列表存放
subject = "菜篮子接口测试报告"  #邮件主题



#存放项目文件的路径
prj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  #当前文件的上一级的上一级目录（增加一级）

#存放接口数据文件的路径
api_data_path = os.path.join(prj_path,"Data","api_test_data.xls")

#存放用例的目录
case_path = os.path.join(prj_path,"TestCase")

#存放日志的目录
log_dir = os.path.join(prj_path, 'Log')

#存放测试报告的目录
report_dir = os.path.join(prj_path,"Report")

#存放测试报告的路径（适用于HTMLTestRunner以及发邮件）
HTML_filename = report_dir+"\\"+time.strftime("%Y-%m-%d %H_%M_%S")+"_ApiTestReport.html"

#配置log格式
logging.basicConfig(level = logging.DEBUG, #log级别
                    format = "[%(asctime)s] %(levelname)s [%(funcName)s %(filename)s %(lineno)d] %(message)s", #log格式
                    datefmt = "%Y-%m-%d %H:%M:%S",  #日期格式
                    filename = log_dir+"\\"+time.strftime("%Y-%m-%d %H_%M_%S")+"_log.txt", #日志输出文件
                    filemode = "w" ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志;a是追加模式，默认如果不写的话，就是追加模式
)




