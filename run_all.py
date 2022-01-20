import logging,unittest,time,sys
from Config import config
from BeautifulReport import BeautifulReport #适合直接在本地看，美观
from HTMLTestRunner import HTMLTestRunner #适合发邮件用，该有的都有
from Lib import send_email,get_newpath
sys.path.append(r"D:\project\cailanzi")

if __name__ == "__main__":
    logging.info("=============测试开始=============")
    suite = unittest.TestLoader().discover(start_dir=config.case_path,pattern="testcase*.py") #源代码写明：defaultTestLoader = TestLoader()
    runner = BeautifulReport(suite)
    runner.report(description="菜篮子接口自动化",filename=time.strftime("%Y-%m-%d %H_%M_%S")+"_ApiTestReport.html",report_dir=config.report_dir)

    #with open(file=config.HTML_filename,mode='wb') as f: # 改为with open 格式
        #HTMLTestRunner(stream=f, title="ApiTestReport", description="菜篮子接口自动化",verbosity=2).run(suite)
    logging.info("=============测试结束=============")
    #获取最新的报告和日志
    new_report_file = get_newpath.getNewPath(config.report_dir)
    new_log_file = get_newpath.getNewPath(config.log_dir)
    #发送邮件
    send_email.sendEmail(new_report_file,new_log_file)


