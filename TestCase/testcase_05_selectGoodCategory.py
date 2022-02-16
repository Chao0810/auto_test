import unittest,requests,json,ddt,sys,logging
from Lib import readExcelData,testcase_log,write_exceldata,logger
from Config import config
sys.path.append(r"D:\project\cailanzi")

data_list = readExcelData.getExceldata(config.api_data_path,config.sh5)
logger = logging.getLogger("mainlog.selectgoodcategory")

@ddt.ddt()
class TestselectGoodCategory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("{}接口用例页开始".format(config.sh5))

    @classmethod
    def tearDownClass(cls):
        logger.info("{}接口用例页结束".format(config.sh5))

    @ddt.data(*data_list)
    def testselectGoodCategory(self,testdata):

        #发送post请求
        res = requests.post(testdata["Url"],json.loads(testdata["Data"]))
        testcase_log.TestCase_Log(testdata["Case_Name"],testdata["Url"],testdata["Data"],testdata["Expect_Res"],res.text)

        #断言
        try:
            self.assertEqual(json.loads(res.text)["result"],json.loads(testdata["Expect_Res"])["result"],msg="断言失败")
            logger.info("测试结果为Pass")
            write_exceldata.writeExcelData(config.api_data_path,config.sh5,int(testdata["Id"]),len(testdata)-1,"Pass")
        except Exception as e:
            logger.info("测试结果为Fail")
            write_exceldata.writeExcelData(config.api_data_path,config.sh5,int(testdata["Id"]),len(testdata)-1,"Fail")
            raise e
        finally:
            write_exceldata.writeExcelData(config.api_data_path,config.sh5,int(testdata["Id"]),len(testdata)-2,res.text)

if __name__ == '__main__':
    unittest.main(verbosity=2)