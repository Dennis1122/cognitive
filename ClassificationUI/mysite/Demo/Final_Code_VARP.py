import sys
import os
sys.path.insert(1,os.getcwd()+"/Demo")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import re
import pickle
import pandas as pd
import numpy as np
import webbrowser
import os
from nltk.corpus import stopwords
import pdfquery
from collections import defaultdict
from PyPDF2 import PdfFileReader
import spacy
import gc
import sys
import nltk
from nltk import tokenize
from nltk.tokenize import word_tokenize
import itertools

clf_bod=joblib.load('C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/Randomforestmodel_model1.pkl')
tf_bod=joblib.load('C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/feature_set1.pickle')

clf_sh=joblib.load('C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/Randomforestmodel_model_SH.pkl')
tf_sh=joblib.load('C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/feature_set_SH.pickle')

nlp = spacy.load('en')


# In[3]:


def read_cordinates1(path):
    PagePosDict=defaultdict()
    page_num=[]
    PageDict=defaultdict()

    """ This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file"""
    pdf=pdfquery.PDFQuery(path)

    pdf_pages = PdfFileReader(open(path,'rb'))
    pages=pdf_pages.getNumPages()
    for i in range(0,pages):
        try:
            pdf.load(i)
            print (i)
            JQuery=pdf.pq('LTPage')
            for j in JQuery("LTTextLineHorizontal"):
                try:
                    PageDict[i].append(JQuery(j).text())
                except KeyError:
                     PageDict[i] = [JQuery(j).text()]

                cordinates=list()
                cordinates.append(i)
                page_num.append(i)
                cord=JQuery(j).attr('bbox')
                for a in ['[',']']:
                    cord = cord.replace(a,'')
                for a in cord.split(', '):
                    cordinates.append(float(a))
                PagePosDict[tuple(cordinates)]=JQuery(j).text()

        except Exception:
            continue

    return PagePosDict,PageDict,page_num



# In[25]:


def nob_extraction(pdf,page_num):

    five_pages={}

    for i,j in pdf.items():
        if i[0]<=7:
            five_pages[i]=j

    regex1 = re.compile('[^a-zA-Z ]')

    p_keyword_data1=pd.read_excel("C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/p_keylist.xls", encoding="ISO-8859-1").dropna()
    p_key_list1 = list(p_keyword_data1["keyword"])
    p_key_list2=[]
    for k in set(p_key_list1):
        k = regex1.sub(' ', k)
        k=k.lower().strip()
        p_key_list2.append(k)

    s_keyword_data1=pd.read_excel("C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/s_keylist.xls", encoding="ISO-8859-1").dropna()
    s_key_list1 = list(s_keyword_data1["keyword"])
    s_key_list2=[]
    for k in set(s_key_list1):
        k = regex1.sub(' ', k)
        k=k.lower().strip()
        s_key_list2.append(k)

    result_list=[]
    result_dict={}

    f_list=[]
    p_sel_key_list=[]
    p_sent=[]
    for i in five_pages.values():
        sentence=[]
        sentence=tokenize.sent_tokenize(i)
        for j in sentence:
            p_key=""
            for k in set(p_key_list2):
                if k.lower() in j.lower():
                    p_key+=k.lower()+" "
            if len(p_key)>0:
                try:
                    result_dict[p_key].append(j)
                except KeyError:
                    result_dict[p_key] = [j]

    if len(result_dict)<1:
        s_sel_key_list=[]
        s_sent=[]
        for i in five_pages.values():
            sentence=[]
            sentence=tokenize.sent_tokenize(i)
            for j in sentence:
                s_key=""
                for k in set(s_key_list2):
                    if k.lower() in j.lower():
                         s_key+=k.lower()+", "
                if len(s_key)>0:
                    try:
                        result_dict[s_key].append(j)
                    except KeyError:
                        result_dict[s_key] = [j]

    return result_dict






# In[26]:


def bod_extraction(pdf,page_num):
    line_set=[]
    exceptionWords=['Statement','Atos','Ms','Mr','Ltd','Health','Ramsay','of','Mathematical',
                    'Physics', 'MEng', 'Petroleum', 'Engineering','CEng','FAICD','MBA', 'the',
                    'nomination', 'MAICD','NSPCC','CA','MA','BA','FCA','Investment','KPMG','Sustainability',
                    'Committee','International','Council','Group','BEng','Foundation','LLB','Business','society',
                    'Airlines','Chemical','maths','Astrophysics','GAICD','FCIS','Hons', 'Diploma','SKYCITY',
                    'Entertainment', 'AXA','Limited','Quali','cations','Universidad','Autonomo','Independence',
                    'Sainsbury','BAA','Audit','Enterprises','Laboratories','Sixth','Science','Technology','Remuneration',
                    'Joint','Chiefs','Applications','Corporation','Teledesic','Holdings','Stock','Exchange',
                    'Blue','University','Star','Non']

    try:
        cleaned_text={}
        for i in set(page_num):
            line=""
            for k,v in pdf.items():
                if i==k[0]:
                    if len(v)>1:
                        line+=v+" "

            cleaned_text[i]=line
        page_set=[]
        result_list=[]
        for num,eachline in (cleaned_text.items()):
            k = eachline
            testVector = tf_bod.transform([eachline])
            result = clf_bod.predict(testVector)
            if result==1:
                page_set.append(str(num))


        new_dict={}
        for i,j in sorted(pdf.items()):
            if str(i[0]) in page_set:
                if len(j.split())>1 and len(j)>4:
                    new_dict[i]=j

        regex1 = re.compile('[^a-zA-Z ]')
        level1=[]
        for i in new_dict.values():
            if len(i)>4:
                name_list=[]
                i=i.replace("\n"," # ")
                for line in i.split("#"):
                    line=line.replace("&","and")
                    line=line.replace("'s "," ")
                    line=line.replace("’s "," ")
                    k= regex1.sub(' ', line)
                    k = ' '.join(word for word in k.split())
                    if 0<len(k.split())<50:
                        for r_words in exceptionWords:
                            for word in k.split():
                                if r_words.lower() == word.lower():
                                    k=k.replace(word," ")

                        doc = nlp(k)
                        for ent in doc.ents:
                            if ent.label_ == 'PERSON':
                                if len(ent.text.strip())>4:
                                    if len(ent.text.split())>1:
                                        name_list.append(ent.text.strip())

                        if 0<len(name_list)<2 or len(name_list)>4:
                            level1.append(name_list)

                names=list(level1 for level1,_ in itertools.groupby(level1))
        new_names=[]
        for line in (names):
            for eachname in line:
                new_names.append(eachname)
        return (new_names, page_set)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        return (page_set)



# In[40]:


def sh_extraction(pdf,page_content,page_num):

    stop = set(stopwords.words('english'))
    line_set=[]

    exceptionWords1=["the committee","executive directors","corporate responsibility","remuneration policy",
                     "remuneration committee","the group","external auditor"]

    try:
        print ("Reading Completed")
        cleaned_text={}
        for i in set(page_num):
            line=""
            for k,v in page_content.items():
                if i==k:
                    if len(v)>0:
                        line=" ".join(v)

            cleaned_text[i]=line

        page_set=[]
        result_list=[]
        for num,eachline in (cleaned_text.items()):
            k = eachline
            testVector = tf_sh.transform([eachline])
            result = clf_sh.predict(testVector)
            if result==1:
                page_set.append(str(num))

        keyword_data = pd.read_excel("C:/Users/1205031/Desktop/DjangoAR/mysite/Demo/shareholders.xls", encoding="ISO-8859-1").dropna()
        keywords = list(keyword_data["keywords"])
        page_req=[]

        for i,j in sorted(page_content.items()):
            if str(i) in page_set:
                for key in keywords:
                    for word in j:
                        if key.lower() in word.lower():
                            page_req.append(i)
        page_dict={}
        for i,j in pdf.items():
            page=i[0]
            if page in page_req:
                page_dict[i]=j
        name_pos_dict={}
        for i,j in page_dict.items():
            line=str(j)
            line=line.replace("'s","s")
            k = ' '.join(word for word in line.split())
            if 1<len(k.split())<=15:
                doc = nlp(k)
                for ent in doc.ents:
                    if ent.label_ == 'PERSON' or ent.label_ == 'ORG':
                        if len(ent.text.strip())>6:
                            if 1<len(ent.text.split())<10:
                                name_pos_dict[i]=(ent.text.strip())
        #print ("1&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        #print (name_pos_dict)
        if len(name_pos_dict)>0:
            result_none=[]
            result={}
            for i,j in sorted(name_pos_dict.items()):
                flag=0
                name=""
                for m,n in sorted(page_dict.items()):
                    if i==m:
                        name=n
                for k, v in sorted(page_dict.items()):
                    if i[0]==k[0] and i[2]-2<=k[2]<=i[2]+2 and i[1]<=k[1]:
                        if i!=k:
                            flag=1
                            try:
                                result[name].append(v)
                            except KeyError:
                                result[name] = [v]
                if flag==0:
                    if len(name.split())<5:
                        letter_count= len(re.findall('[a-zA-Z]',name))
                        num_count= len(re.findall('[0-9]',name))
                        if letter_count<15 and num_count>3:
                            result_none.append(name)
            #print ("2&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #print (result)

            #print ("3&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #print (result_none)
            regex2 = re.compile('[^0-9./ ]')
            new_dict={}
            if len(result)>0:
                for i,j in result.items():
                    flag_check=0
                    for k in j:
                        try:
                            letters= len(re.findall('[a-zA-Z]',k))
                            if letters<3:
                                if not k.isalpha():
                                    k = regex2.sub('', k)
                                    spaces=k.count(" ")
                                    if spaces<1:
                                        if float(k)<100:
                                            k="Percentage: "+str(k)+"%"
                                        else:
                                            k="Number of Shares: "+str(k)
                                        try:
                                            new_dict[i].append(k)
                                        except KeyError:
                                            new_dict[i] = [k]
                            flag_check=1
                        except Exception:
                            continue
                    if flag_check==0:
                        new_dict[i] = "NONE"

            #print ("4&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #print (new_dict)
            return (page_req, new_dict, result_none, 10)

    except Exception as e:
        #print ("Exception!!")
        if len(page_req)>0:
            if len(name_pos_dict)>0:
                return (page_req,name_pos_dict,result_none,2)
            else:
                return (page_req,[],[],1)
        else:
            return ([],[],[],0)


# In[30]:

def main():

    path="C:/Users/1062522/Desktop/sony/electrocomponents-annual-report-2017.pdf"
    pdf,page_content,page_num=read_cordinates1(path)


    # In[41]:


    print ("===================================================================")
    nob_dict={}
    nob_area=nob_extraction(pdf,page_num)
    for i,j in (nob_area.items()):
        area=""
        for line in j:
            area+=line+" "
        nob_dict[i.upper()]=area
    print ("Nature of Business")
    print (nob_dict)
    print ("===================================================================")

    bod, page_bod=bod_extraction(pdf,page_num)
    print ("PageNumber",page_bod)
    print ("Board of Directors")
    print (bod)
    print ("===================================================================")

    page_sh,sh,none_list,success=sh_extraction(pdf,page_content,page_num)

    if success==10:
        print ("Level1")

        sh_page_no=(set(page_sh))
        sh_dict={}
        for i,j in sh.items():
            if str(j)!="NONE":
                detail=", ".join(j)
                sh_dict[i]=detail
        null_list= (none_list)
        names_list=[]

        print ("Page Number: ",sh_page_no)
        print ("ShareHolders")
        print (sh_dict)
        print (null_list)

    elif success==2:
        print ("Level2")

        sh_page_no= (set(page_sh))
        names_list=sh.values()
        sh_dict={}
        null_list=[]

        print ("Page Number: ",sh_page_no)
        print ("ShareHolders")
        print (names_list)

    elif success==1:
        print ("Level3")

        sh_page_no= (set(page_sh))
        names_list=[]
        null_list=[]
        sh_dict={}

        print ("Page Number: ",sh_page_no)

    else:
        print ("No output")
        sh_page_no= []
        null_list=[]
        sh_dict={}
