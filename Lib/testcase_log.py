import json,sys
from Config import config
sys.path.append(r"D:\project\cailanzi")

def TestCase_Log(case_name,url,data,expect_res,res_text):
    if isinstance(data,dict):
        data = json.dumps(data,ensure_ascii=False) #因为序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii=False;json.dumps()将数据变成字符串
    config.logging.info("测试用例：{}".format(case_name))
    config.logging.info("Url：{}".format(url))
    config.logging.info("请求参数：{}".format(data))
    config.logging.info("期望结果：{}".format(expect_res))
    config.logging.info("实际结果：{}".format(res_text))