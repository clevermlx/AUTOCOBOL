# encoding: utf-8

'''
1.读excel 获取参数
2.录入字典->分2个 文件字典 表字典
3.根据division生成不同函数,拼接字符串
4.每一个division后,跟writelines
5.生成段


'''

import xlrd
import os
from autoCobol import *

def main():
    programname = ''
    files = {}
    tables = {}

    # 打开EXCEL
    configexcel = xlrd.open_workbook("/Users/a123145/Desktop/TEMPLATE.xlsx")
    sheet = configexcel.sheets()[0]
    nrows = sheet.nrows
    ncols = sheet.ncols

    for i in range(nrows):
        if i == 0:
            programname = sheet.cell(0, 0).value
        else:
            rw = sheet.cell(i, 1).value
            tf = sheet.cell(i, 2).value
            name = sheet.cell(i, 3).value
            dealtyp = sheet.cell(i, 4).value
            path = '/Users/a123145/PycharmProjects/AOTOCOBOL/'
            if tf == 'F':
               cpypath = GetFileList(path, name.replace('F','C',1))
            else:
               cpypath = GetFileList(path, name,)

            if cpypath != None:
                if tf.upper() == 'T':
                    tables[name] = [rw, dealtyp, cpypath]
                else:
                    files[name] = [rw, dealtyp, cpypath]
            else:
                print 'not found path of %s ' %name

    cobol = autoCobol(programname, tables, files)
    cobol.createprogram()


def GetFileList(dir, filename):
    newDir = dir
    path = None
    if os.path.isdir(dir):
        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码
            # if s == "xxx":
            # continue
            newDir = os.path.join(dir, s)
            if s == (filename + '.TXT'):
                path = newDir
                break
            else:
                path = GetFileList(newDir, filename)
                if path != None:
                    break
    return path

if __name__ == '__main__':
    main()
