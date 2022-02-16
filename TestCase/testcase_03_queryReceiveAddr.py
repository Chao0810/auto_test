import unittest,requests,json,logging,ddt,sys
from Config import config
from Lib import readExcelData,testcase_log,write_exceldata,logger
sys.path.append(r"D:\project\cailanzi")

data_list = readExcelData.getExceldata(config.api_data_path,config.sh3)
logger = logging.getLogger("mainlog.queryreceiveaddr")

@ddt.ddt()
class TestQueryReceiveAddr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("{}接口测试页开始".format(config.sh3))

    @classmethod
    def tearDownClass(cls):
        logger.info("{}接口测试页结束".format(config.sh3))

    @ddt.data(*data_list)
    def testQueryReceiveAddr(self,testdata):

        #发送post请求
        res = requests.post(url=testdata["Url"],data=json.loads(testdata["Data"]))
        testcase_log.TestCase_Log(case_name=testdata['Case_Name'],url=testdata["Url"],data=testdata["Data"],expect_res=testdata["Expect_Res"],res_text=res.text)

        #断言
        try:
            self.assertEqual(json.loads(res.text)["result"],json.loads(testdata["Expect_Res"])["result"],msg="断言失败")
            logger.info("测试结果为Pass")
            write_exceldata.writeExcelData(config.api_data_path,config.sh3,int(testdata["Id"]),len(testdata)-1,"Pass")
        except Exception as e:
            logger.info("测试结果为Fail,具体原因是：{}".format(e))
            write_exceldata.writeExcelData(config.api_data_path,config.sh3,int(testdata["Id"]),len(testdata)-1,"Fail")
            raise e
        finally:
            write_exceldata.writeExcelData(config.api_data_path,config.sh3,int(testdata["Id"]),len(testdata)-2,res.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
