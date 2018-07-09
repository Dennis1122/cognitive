import re
from StringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from sklearn.feature_extraction.text import CountVectorizer
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import pickle
import pdfquery
from collections import defaultdict
import myconfig

""" This pgm will read a pdf and will extract page and cordinate details of text present in the pdf file"""



def read_cordinates(path):
    """ This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file"""
    PagePosDict=defaultdict()
    pdf=pdfquery.PDFQuery(path)
    global PLAINTIFF,DEFENDANT
    i=0
    try:
            while i <=5:
                    pdf.load(i)
                    JQuery=pdf.pq('LTPage')
                    
                    k =  JQuery.attr('bbox')
                    max_cords=[]
                    for a in ['[',']']:
                        k = k.replace(a,'')
                    for a in k.split(', '):
                        max_cords.append(float(a))
                    maxX = max_cords[3]-100
                    #print max_cords[2]
                    
                    if JQuery.text().find('Service of Process Transmittal')>=0 :
                        i+=1
                        continue
                    for j in JQuery("LTTextBoxHorizontal"):
                        cordinates=list()
                        cordinates.append(i)
                        cord=JQuery(j).attr('bbox')
                        for a in ['[',']']:
                            cord = cord.replace(a,'')
                        
                        for a in cord.split(', '):
                            cordinates.append(float(a))
                            
                        Xc = tuple(cordinates)[4]
                        #print Xc
                        if maxX<Xc:
                            #print tuple(cordinates),JQuery(j).text()
                            #PagePosDict[tuple(cordinates)]=JQuery(j).text()
                            cordinates[4],cordinates[3],cordinates[1],cordinates[2]=cordinates[1]\
                            ,cordinates[2],cordinates[4],cordinates[3]
                            PagePosDict[tuple(cordinates)]=JQuery(j).text()
                    i+=1
    except Exception as E:
        return PagePosDict
    return PagePosDict



def header_box(path):
    pdf = read_cordinates(path)
    
    dtaa = sorted(pdf.iteritems(),reverse=True)

    pages = []
    page_wise_lines = []
    page_no = dtaa[0][0][0]
    page_wise_lines.append(dtaa[0])
    for line in range(1,len(dtaa)):
        #print dtaa[line][0][0]
        nxt_page_no = dtaa[line][0][0]
        if page_no==nxt_page_no:
            page_wise_lines.append(dtaa[line])
        else:
            page_no = nxt_page_no
            pages.append(page_wise_lines)
            page_wise_lines = []
            page_wise_lines.append(dtaa[line])
    pages.append(page_wise_lines) 




    box = []

    for item in pages:



        dtaa = item

        while(len(dtaa)!=0):
            fx1 = dtaa[0][0][4] 
            fy1 = dtaa[0][0][3]

            #print fx1, fy1
            S = dtaa[0][1]
            dtaa[0]=0
            for i in range(1,len(dtaa)):
                cx1 = dtaa[i][0][4] 
                cy1 = dtaa[i][0][3] 
                cy2 = dtaa[i][0][1] 
                #print dtaa[i]

                #print "--------------------------- Y diff ",fy1, cy2,fy1-cy2, S,dtaa[i][1]
                if abs(fy1-cy2)<50:
                    #print "X diff ",fx1, cx1,fx1- cx1,S,dtaa[i][1]
                    if abs(fx1-cx1)<105:

                        S = S+" "+dtaa[i][1]
                        #print "===String::",S
                        dtaa[i]=0
                        fx1 = cx1
                        fy1 = cy1

                #print fx1, fy1

            dtaa = filter(lambda a: a != 0, dtaa)
            #print dtaa
            box.append(S) 
            #break
        #break
    return box


def clean_text(data):
    data = data.lower()
    data = u''.join(data).encode('utf-8')
    data = data.replace("\xc2\xa0"," ")
    data = data.replace("\n\n\n"," ")
    data = data.replace("\n\n"," ")
    data = data.replace("\n"," ")
    regex = re.compile('[^a-zA-Z ]')
    data = regex.sub(' ', data)
    data = re.sub(' +',' ',data)
    data = ' '.join(i for i in data.lower().split() if len(i)>1)
    return data


model_path = myconfig.pltfdftd_model
feature_path = myconfig.pltfdftd_feature
vectorizer = pickle.load(open(feature_path, "rb"))
model = joblib.load(model_path)

def plaintiff_levies(filepath):
    #print filepath
    boxes = header_box(filepath)
    for k in boxes:
        X_test = vectorizer.transform([clean_text(k)])
        res = model.predict(X_test)
        
        
        if res[0]=='1':
            cs = max(model.predict_proba(X_test)[0])
            return plaintiff_correction(clean_text(k)) , cs
    return None,0


def plaintiff_correction(plaintiff):
    
    if len(plaintiff)==0:
        return None
    departments = [ "Department Of Revenue Commonwealth Of Kentucky",
                    "Employment Development Department State Of California",
                    "State Of California Board Of Equalization",
                    "Commissioner Of Taxation and Finance Of the State Of New York",
                    "Department Of the Treasury - Internal Revenue Service",
                    "Premiere Credit Of North America, LLC",
                    "Department Of Labor and Industries, State of Washington",
                    "Commissioner Of Taxation and Finance Of the State Of New York",
                    "State Of New Mexico Taxation & Revenue Department"
                  ]
    
    vector = CountVectorizer(binary=True,ngram_range=(1,3))
    vector.fit([plaintiff])
    countmatrix = vector.transform(departments)
    
    count = list(countmatrix.sum(axis=1))
    dept = departments[count.index(max(count))]
    if max(count)==0:
        return plaintiff
    probabilty = float(max(count))/len(dept.split(" "))
    if probabilty>0.72:
        return dept+", Pltf."
    else:
        return plaintiff


