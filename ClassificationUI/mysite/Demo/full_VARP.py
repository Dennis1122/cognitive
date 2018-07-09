import sys
import os
sys.path.insert(1,os.getcwd()+"/Demo")

import csv
import os.path
import shutil
import collections
import pickle
import dateutil.parser
import re
import operator
import numpy as np
import xml.etree.ElementTree as ET
import dateutil.parser as dparser
import datetime as dt
from sklearn.externals import joblib
from itertools import chain
from collections import OrderedDict
from nltk.corpus import stopwords
from collections import defaultdict
from collections import Counter
from itertools import permutations

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def extractContent(filename):
    XMLpath = "C:/Users/denn/Desktop/POCs/Redaction-UI/data/"+filename+"_blocks.xml"
    Lwords_list = []
    PagePosDict1={}
    tree = ET.parse(XMLpath)
    root = tree.getroot()
    page=0
    for child in root:
        for child1 in child:
            cordinates=[]
            cordinates.append(page-1)
            if(child1.tag=='x'):
                x=child1.text
            if(child1.tag=='y'):
                y=child1.text
            if(child1.tag=='w'):
                w=child1.text
            if(child1.tag=='h'):
                h=child1.text
            if(child1.tag=='t'):
                t=child1.text
                cordinates.append(float(y))
                cordinates.append(float(x))
                cordinates.append(float(w))
                cordinates.append(float(h))
                cordinates=tuple(cordinates)
                PagePosDict1[cordinates]=t
        #filename = os.path.splitext(os.path.basename(XMLpath))
        page+=1
    Filepath="C:/Users/denn/Desktop/POCs/Redaction-UI/data/"
    csv_file=open(Filepath+filename+"_blocks.csv", 'a')
    result1=[]
    for i in sorted(PagePosDict1):
        if i not in result1:
            result=PagePosDict1[i]+" "
        #csv_file.write(PagePosDict1[i]+" ")
        result1.append(i)
        for j in sorted(PagePosDict1):
            if int(i[1])==int(j[1]) and i[0]==j[0] and i!=j and j not in result1:
                result1.append(j)
                result=result+PagePosDict1[j]+" "
                #csv_file.write(PagePosDict1[j]+" ")

        if len(result)>0:
            Lwords_list.append(result)
            result=result+"\n"
            #print result
            csv_file.write(result)
        result=""
        #csv_file.write("\n")
    csv_file.close();
    return Lwords_list

def mask_pdf(inpdf_path,outpdf_path,cords):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    # can.drawString(100, 100, "Hello world")
    can.setLineWidth(3)


    for cord in cords:
        x = cord[0]
        y = cord[1]
        width = cord[2]-cord[0]
        height = cord[3]-cord[1]
        can.rect(x, y,width,height, fill=1)
#     can.rect(x1, y1, x2-x1, y2-y1, fill=1)
#     can.rect(58.919, 679.763, x2-x1, y2-y1, fill=1)
    # can.rect(80, 625, 300, 27, fill=1)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    existing_pdf = PdfFileReader(open(inpdf_path, "rb"))
    
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(outpdf_path, "wb")
    output.write(outputStream)
    outputStream.close()
