import unittest,requests,json,ddt,logging,sys
from Config import config
from Lib import db,readExcelData,testcase_log,write_exceldata,logger
sys.path.append(r"D:\project\cailanzi")

data_list = readExcelData.getExceldata(config.api_data_path,config.sh6)
logger = logging.getLogger("mainlog.addOrder")

@ddt.ddt()
class TestaddOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.DataBase = db.DB() #实例化数据库对象
        logger.info("{}接口用例页开始".format(config.sh6))
        requests.post(url="http://192.168.107.135:80/freshO2O/userAdd.action",data={"account":"fc","password":"fc66666","phone":"13349678458","addr":"深圳市南山区沙河街道"})

    @classmethod
    def tearDownClass(cls):
        cls.DataBase.del_db(tab="user",key="account",value="fc") #数据库环境清理
        logger.info("{}接口用例页结束".format(config.sh6))


    @ddt.data(*data_list)
    def testaddOrder(self,testdata):
        #发送post请求
        res = requests.post(testdata["Url"],json.loads(testdata["Data"]))
        testcase_log.TestCase_Log(testdata["Case_Name"],testdata["Url"],json.loads(testdata["Data"]),testdata["Expect_Res"],res.text)

        res_result = json.loads(res.text)["result"] #获取接口返回的result值
        expect_result = json.loads(testdata["Expect_Res"])["result"] #获取预期的result值
        exist = self.DataBase.check_db(tab="indent",key="account",value="fc") #数据库断言值，True/False

        #断言
        try:
            self.assertEqual(res.status_code,200,msg="响应状态码不正常")
            self.assertEqual(res_result,expect_result,msg="与预期的result不符")
            if expect_result == "ok":
                self.assertTrue(exist,msg="数据库中不存在该数据")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh6,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
                self.DataBase.del_db(tab="indent",key="account",value="fc") #数据库环境清理
            else:
                self.assertFalse(exist,msg="数据库中存在该数据")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh6,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
        except Exception as e:
            logger.info("断言异常，测试结果为Fail")
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh6,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
            if exist == True:
                 self.DataBase.del_db(tab="indent",key="account",value="fc") #数据库环境清理
            raise e
        finally:
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh6,row=int(testdata["Id"]),column=len(testdata)-2,value=res.text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
