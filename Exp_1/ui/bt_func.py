from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel
from ui.Ref_bib_Download import Ui_Mainwindow
import requests
import os
import fitz


# 这个类继承界面UI类
class mywindow(QtWidgets.QWidget, Ui_Mainwindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    # 定义槽函数
    def Path(self):
        # read the file and create the filedir
        FilePath = self.lineEdit.text()
        b_loc = FilePath.rfind('\\')
        e_loc = FilePath.find('.pdf')
        TargetPaper = FilePath[b_loc + 1:e_loc].replace(":", "_")
        now_loc = os.getcwd()
        folder = now_loc + '\\' + TargetPaper
        if not os.path.isdir(folder):
            os.mkdir(folder)

        ref_list = GetRefPages(FilePath)
        references_list = GetRefTxt(ref_list)
        L = len(references_list)
        name_list = []
        # 将ref_list中元素逐个处理后加入name_list
        for i in range(L):
            # 1.删除作者名和回车
            if (references_list[i][0] != "["):
                continue
            self.listWidget.addItem(references_list[i].replace("\n", " "))
            # High fidelity video prediction with large stochastic recurrent neural networks
            # High ﬁdelity video prediction with large stochastic recurrent neural networks
            head = references_list[i].find('“')
            tail = references_list[i].find('”', head + 1)
            papername = references_list[i][head + 1:tail - 1]
            # papername = papername.replace("-\n", "")
            # papername = papername.replace("\n", " ")
            papername = papername.replace("ﬁ", "fi")
            papername = papername.replace("ﬂ", "fl")
            papername = papername.replace("ﬃ", "ffi")
            papername = papername.replace("ﬀ", "ff")

            # 2.把空格换成%20用来搜索
            papername = papername.replace(" ", "%20")
            if papername.find("-\n") == -1:
                name_list.append(papername.replace("\n"," "))
            else:
                papername1 = papername.replace("-\n", '-')
                papername1 = papername1.replace("\n", ' ')
                papername2 = papername.replace("-\n", '')
                papername2 = papername2.replace("\n", ' ')
                name_list.append(papername1)
                name_list.append(papername2)
        # download .bib file
        # 1.get URL and download file
        i = 1
        j = 1
        for papername in name_list:
            search_url = "https://dblp.org/search?q=" + papername
            r = requests.get(search_url)
            # print(r.text)
            b_loc = r.text.find("https://dblp.org/img/download.dark.hollow.16x16.png") - 120
            b_loc = r.text.find("https", b_loc)
            e_loc = r.text.find('"', b_loc)
            bib_url = r.text[b_loc:e_loc]
            # https://dblp.org/rec/journals/corr/abs-1812-00568.html?view=bibtex
            # print(bib_url)
            r1 = requests.get(bib_url)
            b_loc = r1.text.find("download as .bib") - 90
            b_loc = r1.text.find("https", b_loc)
            e_loc = r1.text.find('"', b_loc)
            download_url = r1.text[b_loc:e_loc]
            if download_url == '':
                print(str(j) + ".Not Found:  " + papername.replace("%20", " "))
                j = j + 1
                continue
            # print(download_url)
            file = requests.get(download_url, allow_redirects=True)
            # 2.write the file to local
            filename = folder + "\\" + papername.replace(":", "_")
            filename = filename.replace("%20", " ")
            with open(filename + ".bib", "wb") as f:
                f.write(file.content)
                print(str(i) + ".  " + filename.replace("%20", " "))
                i = i + 1
            f.close()
        print("Done")


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
