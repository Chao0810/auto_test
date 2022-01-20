import xlrd,json,sys
from Config import  config
sys.path.append(r"D:\project\cailanzi")


#
# sh = wb.sheet_by_index(0)
# print(sh.nrows)
# print(sh.ncols)
# print(sh.cell(0,0).value)
# print(sh.row_values(0))
# print(dict(zip(sh.row_values(0),sh.row_values(1)))) #将列名和值组装成字典格式，使数据更加清晰

# for i in range(sh.nrows):
#     print(sh.row_values(i))

#一次性读取单个sheet页的所有数据，并形成大列表
def excel_to_list(data_file,sheet):
    data_list = [] #新建空列表，装下所有的Excel数据
    wb = xlrd.open_workbook(data_file) #打开excel
    sh = wb.sheet_by_name(sheet) #获取每个sheet页
    header = sh.row_values(0)  #获取每个sheet页的第一行标题
    for i in range(1,sh.nrows):  #遍历读取第二行的数据
         d = dict(zip(header,sh.row_values(i)))  #将列名和值组装成字典格式，使数据更加清晰
         data_list.append(d)   #组成一个由一个个字典构成的大列表
    return data_list


#方法二：一次性读取单个sheet页的所有数据，并形成大列表
def getExceldata(data_file,sheetname):
    wb = xlrd.open_workbook(data_file) #打开excel
    sh = wb.sheet_by_name(sheetname) #获取每个sheet页
    data_list = []
    for i in range(1,sh.nrows): #第一行的值（下标为0），作为key
        dict = {}
        for j in range(0,sh.ncols):
            dict[sh.cell_value(0,j)]= sh.cell_value(i,j)
        data_list.append(dict)
    return data_list


'''
#查询某条用例的数据是否在所有数据中（数据有可能中途被移除，故需要此函数）
def get_test_data(data_list,case_name):
    for case_data in data_list: #遍历所有数据
        if case_name == case_data["Case_Name"]: #挨个找，如果字典数据中case_name与case_data["Case_Name"]一致，说明找到了
            return case_data
'''

#测试一下代码
if __name__ == "__main__":
    data_list = getExceldata(config.api_data_path,config.sh4)
    data_addr = json.loads(data_list[0]["Data"])["addr"]
    print(type(data_addr))


