import unittest,logging,requests,json,ddt,sys
from Lib import db,readExcelData,testcase_log,write_exceldata,logger,caseAssert
from Config import config
sys.path.append(r"D:\project\cailanzi")

data_list = readExcelData.excel_to_list(config.api_data_path,config.sh2) #获取表2的所有数据
logger = logging.getLogger("mainlog.register")

@ddt.ddt()
class TestRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("{}接口用例页开始".format(config.sh2))

    @classmethod
    def tearDownClass(cls):
        logger.info("{}接口用例页结束".format(config.sh2))

    @ddt.data(*data_list)
    def testRegister(self,testdata):
        DataBase = db.DB() #实例化数据库对象
        data_account = json.loads(testdata["Data"])["account"] #拿取数据中的账户名，并且一次性格式化显示

        #发送注册请求
        res = requests.post(url=testdata["Url"],data=json.loads(testdata["Data"]))
        testcase_log.TestCase_Log(case_name=testdata["Case_Name"],url=testdata["Url"],data=testdata["Data"],expect_res=testdata["Expect_Res"],res_text=res.text)
        res_result = json.loads(res.text)["result"] #获取接口返回的result值
        expect_result = json.loads(testdata["Expect_Res"])["result"] #获取预期的result值
        exist = DataBase.check_db(tab="user",key="account",value=data_account) #数据库断言值，True/False

        #断言
        try:
            self.assertEqual(res.status_code,200,msg="响应码错误")
            self.assertEqual(res_result,expect_result,msg="与预期的result不相等")
            if expect_result == "ok":
                self.assertTrue(exist,msg="数据库中本应存在该数据，却不存在")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh2,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
                DataBase.del_db(tab="user",key="account",value=data_account) #数据库环境清理
            else:
                self.assertFalse(exist,msg="数据库中本不应存在该数据，却存在")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh2,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
        except Exception as e:
            logger.info("断言异常，测试结果为Fail")
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh2,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
            if exist == True:
                DataBase.del_db(tab="user",key="account",value=data_account) #数据库环境清理
            raise e
        finally:
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh2,row=int(testdata["Id"]),column=len(testdata)-2,value=res.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)