'''
此接口设计有问题
'''
import unittest,logging,requests,json,ddt,sys
from Lib import db,readExcelData,testcase_log,write_exceldata,logger
from Config import config
sys.path.append(r"D:\project\cailanzi")

data_list = readExcelData.excel_to_list(config.api_data_path,config.sh4) #获取表4的所有数据
logger = logging.getLogger("mainlog.addreceiveaddr")

@ddt.ddt()
@unittest.skip
class TestaddReceiveAddr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("{}接口用例页开始".format(config.sh4))
        cls.DataBase = db.DB() #实例化数据库对象
        requests.post(url="http://192.168.107.135:80/freshO2O/userAdd.action",data={"account":"fc","password":"fc66666","phone":"13349678458","addr":"深圳市南山区沙河街道"})

    @classmethod
    def tearDownClass(cls):
        cls.DataBase.del_db(tab="user",key="account",value="fc") #数据库环境清理
        logger.info("{}接口用例页结束".format(config.sh4))

    @ddt.data(*data_list)
    def testRegister(self,testdata):

        #发送收货地址请求
        res = requests.post(url=testdata["Url"],data=json.loads(testdata["Data"]))
        testcase_log.TestCase_Log(case_name=testdata["Case_Name"],url=testdata["Url"],data=testdata["Data"],expect_res=testdata["Expect_Res"],res_text=res.text)
        res_result = json.loads(res.text)["result"] #获取接口返回的result值
        expect_result = json.loads(testdata["Expect_Res"])["result"] #获取预期的result值
        #exist = DataBase.check_db(tab="receiveaddr",key="address",value=data_addr) #数据库断言值，True/False

        #断言
        try:
            self.assertEqual(res_result,expect_result,msg="result不相等")
            logger.info("测试结果为Pass")
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh4,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
            #DataBase.del_db(tab="receiveaddr",key="address",value=data_addr) #数据库环境清理
        except Exception as e:
            logger.info("测试结果为Fail")
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh4,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
            raise e
        finally:
            write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=config.sh4,row=int(testdata["Id"]),column=len(testdata)-2,value=res.text)




if __name__ == "__main__":
    unittest.main(verbosity=2)