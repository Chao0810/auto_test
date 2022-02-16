import unittest,requests,json,ddt,sys,logging
from Lib import db,readExcelData,testcase_log,write_exceldata,logger
from Config import config
sys.path.append(r"D:\project\cailanzi")

data_list = readExcelData.getExceldata(config.api_data_path,config.sh9)
logger = logging.getLogger("mainlog.finishorder")

@ddt.ddt()
class TestunfinishOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.DataBase = db.DB() #实例化数据库对象
        logger.info("{}接口用例页开始".format(config.sh9))
        requests.post(url="http://192.168.107.135:80/freshO2O/orderAdd.action",data={"orderStr":"fu,8,猪肉,23.0,1,深圳市宝安区中南花园"})

    @classmethod
    def tearDownClass(cls):
        cls.DataBase.del_db(tab="indent",key="account",value="fu") #数据库环境清理
        logger.info("{}接口用例页结束".format(config.sh9))

    @ddt.data(*data_list)
    def testselectOrder(self,testdata):

        #发送post请求
        res = requests.post(testdata["Url"],json.loads(testdata["Data"]))
        testcase_log.TestCase_Log(testdata["Case_Name"],testdata["Url"],json.loads(testdata["Data"]),testdata["Expect_Res"],res.text)

        res_result = json.loads(res.text)["result"] #获取接口返回的result值
        expect_result = json.loads(testdata["Expect_Res"])["result"] #获取预期的result值
        exist = self.DataBase.check_sth_db(cloum="o_state",tab="indent",key="account",value="fu") #数据库断言值

        #断言
        try:
            self.assertEqual(res.status_code,200,msg="响应状态码不正常")
            self.assertEqual(res_result,expect_result,msg="与预期的result不符")
            if expect_result == "已完成":
                self.assertEqual(exist[0][0],"已完成",msg="数据库中订单状态错误")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh9,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
                self.DataBase.updata_db(sql="update indent set o_state='已付款' where account='fu'") #数据库环境复原
            else:
                self.assertNotEqual(exist[0][0],"已完成",msg="数据库中订单状态遭改变")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh9,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
        except Exception as e:
            logger.info("断言异常，测试结果为Fail")
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh9,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
            if exist[0][0] == "已完成":
                 self.DataBase.updata_db(sql="update indent set o_state='已付款' where account='fu'") #数据库环境复原
            raise e
        finally:
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh9,row=int(testdata["Id"]),column=len(testdata)-2,value=res.text)


if __name__ == '__main__':
    unittest.main(verbosity=2)


