'''
Python中发送邮件需要通过Email的smtp服务发送。首先需要确认用来发送邮件的邮箱是否启用了smtp服务
'''
import smtplib,os,sys #用于建立smtp连接
from email.mime.text import MIMEText  #邮件需要专门的MIME格式
from email.mime.multipart import MIMEMultipart  #混合MIME格式，支持上传附件
from email.header import Header  #用于使用中文邮件主题
from Config import config
from Lib import get_newpath
sys.path.append(r"D:\project\cailanzi")

def sendEmail(new_report_file,new_log_file):

    #读取邮件内容
    with open(file=new_report_file,encoding="utf-8") as fp: #打开html报告
         email_body = fp.read() #读取报告内容
    #读取日志内容
    with open(file=new_log_file,encoding="utf-8") as fp2: #打开日志文件
         log_body = fp2.read() #读取日志文件
    #读取接口用例的Excel表格
    with open(file=config.api_data_path,mode="rb") as fp3: #打开接口用例的Excel表格(rb操作时不支持指定encoding参数)
         excel_body = fp3.read() #读取接口用例的Excel表格

    msg = MIMEMultipart() #混合MIME格式,添加一个MIMEmultipart类，处理正文及附件

    #组装Email(发件人，收件人，邮件主题);符合 MIME 的标头
    msg["Subject"] = Header(s=config.subject,charset="utf-8")  #中文邮件主题，指定编码方式
    msg["From"] = Header(s=config.sender) #发送方
    msg["To"] = Header(s=",".join(config.receiver)) #两个及以上的接收方

    #添加html格式邮件正文，样式会丢失
    part1 = MIMEText(_text=email_body,_subtype="html",_charset="utf-8")

    #添加附件
    part2 = MIMEText(_text=log_body,_subtype="plain",_charset="utf-8")
    part2["Content-Type"] = "application/octet-stream" #附件设置内容类型，方便起见，设置为二进制流(此标头的附加参数取自关键字参数。)
    part2["Content-Disposition"] = "attachment;filename={}".format(os.path.split(new_log_file)[1]) #设置附件头，添加文件名log.txt( os.path.split()以元组存放 )

    #添加接口用例的Excel表格附件
    part3 = MIMEText(_text=excel_body,_subtype="plain",_charset="utf-8")
    part3["Content-Type"] = "application/octet-stream" #附件设置内容类型，方便起见，设置为二进制流
    part3["Content-Disposition"] = "attachment;filename='api_test_data.xls'" #设置附件头，添加文件名

    #添加html报告附件
    part4 = MIMEText(_text=email_body,_subtype="html",_charset="utf-8")
    part4["Content-Type"] = "application/octet-stream" #附件设置内容类型，方便起见，设置为二进制流(此标头的附加参数取自关键字参数。)
    part4["Content-Disposition"] = "attachment;filename={}".format(os.path.split(new_report_file)[1])

    #将内容和附件添加到邮件主体中
    msg.attach(part1)
    msg.attach(part2)
    msg.attach(part3)
    msg.attach(part4)

    #发邮件,并且进行断言
    try:
        smtp = smtplib.SMTP_SSL(host=config.smtp_server,port=config.smtp_port)
        smtp.login(config.smtp_user,config.smtp_password)
        smtp.sendmail(config.sender,config.receiver,msg.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败！具体原因是：{}".format(e))
    finally:
        smtp.quit()


if __name__ == "__main__":
    report_file = get_newpath.getNewPath(config.report_dir)
    log_file = get_newpath.getNewPath(config.log_dir)
    sendEmail(report_file,log_file)





