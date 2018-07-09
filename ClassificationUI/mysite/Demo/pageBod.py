import sys
import os
sys.path.insert(1,os.getcwd()+"/Demo")

import pandas as pd
import os
import time
#data_file=pd.read_excel("Demo_excel.xls")
#data_file=pd.read_excel("Demo_excel.xls",encoding="ISO-8859-1").dropna()
data_file=pd.read_excel("demo_shareholder.xls",encoding="ISO-8859-1").dropna()
documents = list(data_file["documents"])
pages = list(data_file["pages"])
bod= list(data_file["shareholders"])

def page_bod(path):
    doc_name=path.split("\\")[-1]
    print("---",doc_name)
    print("===",documents,len(documents))
    for i in documents:
        if doc_name==i:
            req_doc=documents.index(i)
    
    p=pages[req_doc]
    b=bod[req_doc]
    page_list=[]
    p=str(p)
    for i in p.split(","):
        page_list.append(i)
    bod_list=[]
    b=str(b)
    for i in b.split("\n"):
        bod_list.append(i)
    #time.sleep(7)
    return page_list, bod_list
