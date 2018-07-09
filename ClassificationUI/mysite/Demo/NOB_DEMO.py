import sys
import os
sys.path.insert(1,os.getcwd()+"/Demo")
import pandas as pd
import re
import pdfquery
from collections import defaultdict
import nltk
from nltk import word_tokenize
from nltk.util import ngrams
import os
from nltk.corpus import stopwords




def read_cordinates12(path):
    PagePosDict=defaultdict()
   
    
    """ This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file"""
    pdf=pdfquery.PDFQuery(path)

    for i in range(0,5):
        try:
            pdf.load(i)
            print (i)
            JQuery=pdf.pq('LTPage')
            
            for j in JQuery("LTTextBoxHorizontal"):
                cordinates=list()
                cordinates.append(i)
               
                cord=JQuery(j).attr('bbox')
                for a in ['[',']']:
                    cord = cord.replace(a,'')
                for a in cord.split(', '):
                    cordinates.append(float(a))
                PagePosDict[tuple(cordinates)]=JQuery(j).text() 
                
                
        except Exception:
            continue
            
    return PagePosDict






def nob_extraction(path):

    regex1 = re.compile('[^a-zA-Z ]')

    p_keyword_data1=pd.read_excel(r"D:/SANAL/DjangoAR/mysite/Demo/static/Demo/pdfs/varp/p_keylist.xls", encoding="ISO-8859-1").dropna()
    p_key_list1 = list(p_keyword_data1["keyword"])
    p_key_list2=[]
    for k in set(p_key_list1):
        k = regex1.sub(' ', k)
        k=k.lower().strip()
        p_key_list2.append(k)

    s_keyword_data1=pd.read_excel(r"D:/SANAL/DjangoAR/mysite/Demo/static/Demo/pdfs/varp/s_keylist.xls", encoding="ISO-8859-1").dropna()
    s_key_list1 = list(s_keyword_data1["keyword"])
    s_key_list2=[]
    for k in set(s_key_list1):
        k = regex1.sub(' ', k)
        k=k.lower().strip()
        s_key_list2.append(k)

    result_list=[]
    
    pdf=read_cordinates12(path)
    f_list=[]
    p_sel_key_list=[]
    for i in pdf.values():
        for k in set(p_key_list2):
            if k.lower() in i.lower():
                p_sel_key_list.append(k.lower())

             

    if len(set(p_sel_key_list))<1:
        s_sel_key_list=[]
        for i in pdf.values():
            for k in set(s_key_list2):
                if k.lower() in i.lower():
                    s_sel_key_list.append(k.lower())
        result_list=(set(s_sel_key_list))
    else:
        result_list=(set(p_sel_key_list))

    r_list=[]
    for i in result_list:
        i=i.strip().title()
        r_list.append(i)
        
    return r_list
        
    print ("#################################")














