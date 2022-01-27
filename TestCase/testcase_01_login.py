import unittest,logging,json,requests,ddt,sys
from Config import config
from Lib import readExcelData,testcase_log,write_exceldata,logger
sys.path.append(r"D:\project\cailanzi")


data_list = readExcelData.getExceldata(config.api_data_path,config.sh1) #得到sh1的全部数据，由一个个字典构成的大列表
logger = logging.getLogger("mainlog.login")

@ddt.ddt() #装饰类，也就是继承TestCase的类
class TestLoginApi(unittest.TestCase): # 类必须以Test开头，继承TestCase才能识别为用例类

    @classmethod # 声明为类方法（必须）
    def setUpClass(cls): # 类方法，注意后面是cls（也可以是self），整个类只执行一次
       logger.info("{}接口用例页开始".format(config.sh1))


    @ddt.data(*data_list) #装饰测试方法
    def testLogin(self,testdata): #testdata代表传入的每条参数
         res = requests.get(url=testdata["Url"],params=json.loads(testdata["Data"])) #get请求,此时data为字符串格式，需要用json.loads()转化为字典格式
         testcase_log.TestCase_Log(case_name=testdata["Case_Name"],url=testdata["Url"],data=testdata["Data"],expect_res=testdata["Expect_Res"],res_text=res.text) #输出相应用例log
         try:
             self.assertEqual(json.loads(res.text)["result"],json.loads(testdata["Expect_Res"])["result"],msg="断言失败")
             logger.info("测试结果为Pass")
             write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh1,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
         except Exception as e:
             logger.info("测试结果为Fail,具体原因是：{}".format(e))
             write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh1,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
             raise e
         finally:
             write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh1,row=int(testdata["Id"]),column=len(testdata)-2,value=res.text)


    @classmethod
    def tearDownClass(cls):
        logger.info("{}接口用例页结束".format(config.sh1))


if __name__ == "__main__": # 非必要，用于测试代码
    unittest.main(verbosity=2) #右键此处，才会运行整个py文件！