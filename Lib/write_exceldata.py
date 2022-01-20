'''
xlrd只能读取表格，不能直接修改原表格，复制原表格之后可以修改。支持xlsx, xls文件格式
xlwt只能修改表格，不能读取表格，支持xlsx, xls文件格式
xlutils可以将xlrd.Book转为xlwt.Workbook，从而可以
'''

from xlutils.copy import copy
import xlrd,sys
sys.path.append(r"D:\project\cailanzi")

def writeExcelData(datafile,sheetname,row,column,value):
    wb = xlrd.open_workbook(datafile,formatting_info=True) #open_workbook()内若没有添加formatting_info=True，则保存的文件不会保留原有格式
    new_wb = copy(wb) #因为同一个文件不能同时又读又写，这里先拷贝出这个文件，改好了再覆盖原文件
    new_sh = new_wb.get_sheet(sheetname) #通过sheetname获取想要的sheet页
    new_sh.write(row,column,value) #在某行某列，写入内容
    new_wb.save(datafile)  #覆盖原来的文件
    return True