import unittest,requests,json,ddt,logging,sys
from Config import config
from Lib import db,readExcelData,testcase_log,write_exceldata,logger
sys.path.append(r"D:\project\cailanzi")

#若测试改动了数据库的数据，就用此断言方法
def change_db_assert(logger,res_result,expect_result,exist,DataBase,tab,key,value,sheetname,testdata,res_text):
    '''
    :param logger 日志记录器
    :param res_result 响应中“result”的值
    :param expect_result 期望“result”的值
    :param exist 是否已存在于数据库，True/False
    :param DataBase 数据库名
    :param tab 数据库中具体哪个表
    :param key 表中的列名
    :param value 表中的某个值
    :param sheetname excel表格的sheet名
    :param testdata  测试数据，一般是字典
    :param res_text  响应的文本内容
    '''

    if res_result == expect_result:
        if expect_result == "ok":
            try:
                assert exist == True,"数据库中不存在该数据" #,msg="数据库中不存在该数据")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=sheetname,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
                DataBase.del_db(tab=tab,key=key,value=value) #数据库环境清理
            except Exception as e:
                logger.info("数据库中不存在该数据，测试结果为Fail")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=sheetname,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
                raise e
        else:
            try:
                assert exist == False,"数据库中不存在该数据" #assertFalse(exist,msg="数据库中不存在该数据")
                logger.info("测试结果为Pass")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=sheetname,row=int(testdata["Id"]),column=len(testdata)-1,value="Pass")
            except Exception as e:
                logger.info("本该写入失败，但却成功了，测试结果为Fail")
                write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=sheetname,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
                DataBase.del_db(tab=tab,key=key,value=value) #数据库环境清理
                raise e
    else:
        logger.info("与预期结果不符，测试结果为Fail")
        write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=sheetname,row=int(testdata["Id"]),column=len(testdata)-1,value="Fail")
        if exist == True:
             DataBase.del_db(tab=tab,key=key,value=value) #数据库环境清理


    write_exceldata.writeExcelData(datafile=config.api_data_path,sheetname=sheetname,row=int(testdata["Id"]),column=len(testdata)-2,value=res_text)


#若测试没有改动了数据库的数据，就用此断言方法
def not_change_db_assert(logger,sheetname,testdata,res_text):
    '''
    :param logger 日志记录器
    :param sheetname excel表格的sheet名
    :param testdata  测试数据，一般是字典
    :param res_text  响应的文本内容
    '''
    try:
        assert json.loads(res_text)["result"] == json.loads(testdata["Expect_Res"])["result"],"断言失败,result值与预期不符"
        logger.info("测试结果为Pass")
        write_exceldata.writeExcelData(config.api_data_path,sheetname,int(testdata["Id"]),len(testdata)-1,"Pass")
    except Exception as e:
        logger.info("测试结果为Fail")
        write_exceldata.writeExcelData(config.api_data_path,sheetname,int(testdata["Id"]),len(testdata)-1,"Fail")
        raise e
    finally:
        write_exceldata.writeExcelData(config.api_data_path,sheetname,int(testdata["Id"]),len(testdata)-2,res_text)


if __name__ == '__main__':
    exist=False
    assert exist == True,"数据库中不存在该数据"