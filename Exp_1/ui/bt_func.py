from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel
from ui.Ref_bib_Download import Ui_Mainwindow
import requests

import re
# PyMuPDF
import fitz
import pandas as pd


# 这个类继承界面UI类
class mywindow(QtWidgets.QWidget, Ui_Mainwindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    # 定义槽函数
    def Path(self):
        FilePath = self.lineEdit.text()
        ref_list = GetRefPages(FilePath)
        references_list = GetRefTxt(ref_list)
        L = len(references_list)
        name_list = []
        # 将ref_list中元素逐个处理后加入name_list
        for i in range(L):
            # 1.删除作者名和回车
            if(references_list[i][0]!="["):
                continue
            head = references_list[i].find('“')
            tail = references_list[i].find('”', head + 1)
            papername = references_list[i][head + 1:tail - 1]
            papername = papername.replace("\n", " ")
            self.listWidget.addItem(references_list[i].replace("\n"," "))
            # 2.把空格换成%20用来搜索
            papername = papername.replace(" ", "%20")
            name_list.append(papername)
        #在listview中显示文献名称

        # print(name_list)


# 获取从references开始及之后的页面内容
def GetRefPages(pdfname):
    pdf = fitz.open(pdfname)
    pagenum = len(pdf)
    ref_list = []
    for num, p in enumerate(pdf):
        content = p.get_text('blocks')
        # print(num)
        for pc in content:
            # print(pc)
            txtblocks = list(pc[4:-2])
            txt = ''.join(txtblocks)
            if 'References' in txt or 'REFERENCES' in txt or 'referenCes' in txt:
                refpagenum = [i for i in range(num, pagenum)]
                for rpn in refpagenum:
                    refpage = pdf[rpn]
                    refcontent = refpage.get_text('blocks')
                    for n, refc in enumerate(refcontent):
                        txtblocks = list(refc[4:-2])
                        # 将文献名转换成可供搜索的形式：把空格换成%20，去掉\n
                        ref_list.extend(txtblocks)
    # print(''.join(ref_list))
    return ref_list


# 获取从references之后的文本内容
def GetRefTxt(ref_list):
    refnum = 0
    for nref, ref in enumerate(ref_list):
        if 'References' in ref or 'REFERENCES' in ref or 'referenCes' in ref:
            refnum = nref
    references_list = ref_list[refnum + 1:]
    # print(''.join(references_list))
    return references_list
