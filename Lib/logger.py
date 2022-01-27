import logging,time
from Config import config

#创建一个日志器
logger = logging.getLogger("mainlog") #多次使用相同名称来调用getLogger，返回的是同一个对象的引用。

#创建控制台handler和文本handler,用于输出到控制台和日志文件
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename=config.log_dir+"\\"+time.strftime("%Y-%m-%d %H_%M_%S")+"_log.txt",mode="w",encoding="UTF-8")

#将两个handler放入日志器中
logger.addHandler(console_handler)
logger.addHandler(file_handler)

#设定需要记录的日志级别
logger.setLevel(logging.DEBUG)
#设定日志的格式
log_format = logging.Formatter("[%(asctime)s] %(levelname)s [%(funcName)s %(filename)s %(lineno)d] %(message)s")
#将格式放入handler中
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)


if __name__ == '__main__':
    logger.info("66666")



