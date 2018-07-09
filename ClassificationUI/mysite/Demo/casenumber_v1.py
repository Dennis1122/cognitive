# -*- coding: utf-8 -*-
import pdfquery
import re
from sklearn.externals import joblib
from textblob import TextBlob
from collections import defaultdict
import json
import myconfig
from loger import logger
import warnings
import Error_Handler

# """
# This function is to get the cordinates of the nearby text of the provided locations
#    : params PagePosDict: Dictionary of texts and their respective cordinates
#    : params locations: List of cordinates of the keywords
#    : params xbias: Offset value on x axis
#    : params ybias: Offset value on y axis
#    : return: List of cordinates of the text around the keyword

# """
vect=joblib.load(myconfig.case_tfidf2)
Model=joblib.load(myconfig.case_model_ngram2)
vect1=joblib.load(myconfig.case_tfidf1)
Model1=joblib.load(myconfig.case_model_ngram1)
clf2 = joblib.load(myconfig.case_model_path)
text_vectorizer = joblib.load(myconfig.case_feature_path)
class CaseNumber:
    
    def __init__(self,esop_id, pdf_readLine,pdf_readBox,pdf_readCord):
         with warnings.catch_warnings():
           warnings.simplefilter("ignore", category=UserWarning)
           self.esop_id = esop_id
           self.pdf_readLine = pdf_readLine
           self.pdf_readBox = pdf_readBox
           self.pdf_readCord = pdf_readCord

        # """
        # Count the number of 1's in the given input string
        #    :param inputString: extracted data
        #    :return :number of 1's (Int)
        # """

    def number_of_char(self, inputString, char='1'):
        return (inputString.count(char))
    
    def pre_process(self,text):
        text = text.lower()
        text = text.replace("\n"," ")
        text = text.replace("#"," hashchar ")
        text = re.sub(' +', ' ', text)
        return text

    def search_text_near_locations(self,PagePosDict, locations, xbias=50, ybias=50):
        nearby_locations = []
        for loc in locations:
            x_min = loc[1] - xbias
            x_max = loc[3] + xbias
            y_min = loc[2] - ybias
            y_max = loc[4] + ybias
            for key in PagePosDict.keys():
                if key[0] == loc[0] and key != loc:
                    x = (key[1] + key[3]) / 2
                    y = (key[2] + key[4]) / 2
                    if x >= x_min and x <= x_max and y >= y_min and y <= y_max:
                        nearby_locations.append(key)

        return nearby_locations


    # """
    # This function check whether the input string contain numbers
    #    :param inputString: extracted data
    #    :return :True or False
    # """
    def hasNumbers(self,inputString):
        return any(char.isdigit() for char in inputString)


    # """
    # This function clean up the text by removing the unnecessary characters
    #    :params PagePosDict:Dictionary of text and their respective cordinates
    #    :return: cleaned contents
    # """
    def clean_text(self, PagePosDict):
        doc_contents = []
        contents = []
        doc_keys = []
        test = defaultdict()
        for key in sorted(PagePosDict):
            try:
                txt = PagePosDict[key]
                test[key] = PagePosDict[key]
                regex = re.compile('[^a-zA-Z0-9 ]')
                data = regex.sub(' ', txt)
                data = data.replace("\xa7\xc2\xa0", " ")
                data = data.replace("\n\n\n", " ")
                data = re.sub(' +', ' ', data)
                doc_contents.append(data)
                doc_keys.append(key)
                PagePosDict[key] = data
            except Exception:
                pass
        for cordinate, txt in zip(doc_keys, doc_contents):
            if self.hasNumbers(txt) == False:
                continue
            nearby_locs = self.search_text_near_locations(PagePosDict, [cordinate])
            nearby_txt = ""
            for locs in nearby_locs:
                nearby_txt += PagePosDict[locs]
                nearby_txt += " "
            content = txt + " " + nearby_txt + "," + test[cordinate] + ",\n"
            contents.append(content)

        return contents


    # """
    # This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file
    #  :param path: Directory of the files
    #  :return:Dictionary of words and their corresponding cordinates
    # """

    def read_cordinates(self, path):
        PagePosDict = defaultdict()
        pdf = pdfquery.PDFQuery(path)
        i = 0
        try:
            while i <= 30:
                pdf.load(i)
                JQuery = pdf.pq('LTPage')
                if JQuery.text().find('Service of Process Transmittal') >= 0:
                    i+=1
                    continue
                for j in JQuery("LTTextLineHorizontal"):
                    cordinates = list()
                    cordinates.append(i)
                    cord = JQuery(j).attr('bbox')
                    for a in ['[', ']']:
                        cord = cord.replace(a, '')
                    for a in cord.split(', '):
                        cordinates.append(float(a))
                    PagePosDict[tuple(cordinates)] = JQuery(j).text()
                i += 1
        except Exception:
            pass
        return PagePosDict
    
    # """
    # This function will read PDF contents for the first 30 pages in line and box
    #  :param path: Directory of the files
    #  :return:Dictionary of words in line and box
    # """

    
    def PDFReader(self,path):
        PagePosDict=[]
        PagePosDict1=[]
        pdf=pdfquery.PDFQuery(path)
        i=0
        try:
            while i <=30:
                pdf.load(i)
                JQuery=pdf.pq('LTPage')
                if JQuery.text().find('Service of Process Transmittal')>=0:
                    i+=1
                    continue
                for j in JQuery("LTTextLineHorizontal"):
                    PagePosDict.append(JQuery(j).text())
                for j in JQuery("LTTextBoxHorizontal"):
                    PagePosDict1.append(JQuery(j).text())
                i+=1
        except Exception,e: 
            return PagePosDict,PagePosDict1
        return PagePosDict,PagePosDict1

    # """
    # This function counts the number of digits present in the input string provided
    #    :param inputString:extracted data
    #    :return :count
    # """

    def numberOfDigits(self, inputString):
        count = 0
        for char in inputString:
            if (char.isdigit()):
                count += 1
        return count


    # """
    # This function checks whether the input string contains any lowercase characters
    #    :param inputString: Extracted data
    #   :return :True or False
    # """

    def has_lower_char(self, inputString1):
        spl_words=["false","id","ssn","nj","you","no","nos","cplr",'proc','idx',"am","pm","mi","response","ext","by","for",'box',"to","apr","may","jan","feb","mar","jun","jul","aug","sep","oct","nov","dec","div","ave","tx","garnishment","docket","fax","bb","in","and","my","we","are","the","was","on","his","at","inc","of","rev","ao"]
        char = ""
        for word in spl_words:
            if inputString1.lower() == word:
                return True
        if inputString1.find("$")>=0 or inputString1.find("§")>=0:
            return True
        if self.number_of_char(inputString1.lower(), 'x') > 4 or self.number_of_char(inputString1.lower(),
                                                                                     '1') > 5 or self.number_of_char(
            inputString1.lower(), 'i') > 5:
            return True
        if len(inputString1) > 4:
            if (any(char.islower() for char in inputString1) == True):
                sub1 = inputString1[inputString1.find(char):]
                if self.hasNumbers(sub1) == False:
                    return True
        if len(inputString1) > 3:
            if inputString1 == "CONS":
                return False
            inputString1 = inputString1.replace("/", "")
            test = str(inputString1.lower()) + "qq"
            b = TextBlob(test)
            try:
                if (b.correct() == test):
                    return False
                else:
                    return True
            except Exception:
                return False
        else:
            return False


    """
    This function counts the number of characters in the  input string provided
     :params inputString: Extracted data
     :params char='1':Character constant
     :return:count
    """




    """
    This function extracts the case number attribute from the input string provided
        :param inputString: Extracted data
        :return :case number
    """

    def extract_case_number(self, inputString):
        punctuation = re.compile(r'[.•?!,":;|]')
        inputString = inputString.replace("(cid:9)", " ")
        inputString = inputString.replace("cid 9", " ")
        inputString = inputString.replace("#", "false ")

        data = punctuation.sub(' ', inputString)
        
        data = u''.join(data).encode('utf-8').strip()
        data = data.replace("\xc2\xa0\xa7", " ")
        data = data.replace("\xc2", " ")
        data = data.replace("\xa0", " ")
        data = data.replace("\xa7", " ")
        data = re.compile(r' - ').sub('', data)
        data = re.compile(r'[_()-]').sub('', data)

        data = data.replace("\n\n\n", " ")
        regex = re.compile('[^a-zA-Z0-9$§ ]')
        data = regex.sub(' ', data)
        
        data1 = (data.split(" "))

        for words in data1:
            a = data1.index(words)
            try:
                if (self.has_lower_char(data1[a])):
                    data = re.sub(data1[a], "false ", data, 1)
                    if data1[a].find("$")>=0:
                      data=data.replace(data1[a],"false")
            except Exception:
                pass

        data = data.strip()
        data3 = data.split("false")
        data2 = ""
        for data1 in data3:
            data1 = re.sub(' +', ' ', data1)
            data1 = data1.replace(" ", "")
            data1 = data1.strip()
            if len(data1) > len(data2):
                data2 = data1
        word2 = data2

        if self.hasNumbers(word2) and len(word2) >= 5 and self.numberOfDigits(word2)  >=3 and len(word2)<23:
            word2 = word2.replace("/", "")
            return word2.upper()
        else:
            return ""

    def predict(self):
      try:
        logger.info("starting case number prediction " + str(self.esop_id))
        cs1 = 0
        case_number = '######'
        
        flag = False
        pdf1=self.pdf_readLine
        pdf2=self.pdf_readBox
        
        case1=""
        scr=""
        data_line=[]
        for each in pdf1:
            line = self.pre_process(each)
            data_line.append(line)
        if len(data_line)>0:
            Xtest = vect.transform(data_line)
            result_line = Model.predict(Xtest)
            scr_line= Model.predict_proba(Xtest)
            c=0
            while c<len(data_line):
                if result_line[c]==1:
                    case= self.extract_case_number(data_line[c])
                    if case!="":
                        case1+=case+" "
                        scr+=str(max(scr_line[c]))+" "
                c+=1
            if case1.strip()=="":
                data=[]
                for each in pdf2:
                    line = self.pre_process(each)
                    data.append(line)
                if len(data)>0:
                    Xtest = vect.transform(data)
                    result = Model.predict(Xtest)
                    scr_box = Model.predict_proba(Xtest)
                    c=0
                    while c<len(data):
                        if result[c]==1:
                           
                            if data[c].find("dfs-sop")>=0:
                                data[c]=data[c-1]
                            case= self.extract_case_number(data[c])
                            if case!="":
                                case1+=case+" "
                                scr+=str(max(scr_box[c]))+" "
                        c+=1
            if case1.strip()=="":
                c=0
                while c<len(data_line):
                    if result_line[c]==1:
                        case= self.extract_case_number(' '.join(data_line[c-2:c+2]))
                        if case!="":
                            case1+=case+" "
                            scr+=str(max(scr_line[c]))+" "
                    c+=1
            
            if case1.strip()=="":    
                PagePosDict = self.pdf_readCord
                fd_train=self.clean_text(PagePosDict)
                Y=[]
                X=[]
                result=[]
                nearby_txt=[]
                doc_contents=[]
                check=[]

                regex = re.compile('[0-9]+')
                for txt in fd_train:
                    contents=txt.split(',')
                    temp=[]
                    try:
                        text = contents[0]
                        text=text.replace("(cid:9)","")
                        net_content='"'+contents[1]+'",'
                        doc_contents.append(net_content)
                        data = regex.sub('<num>', text)
                        
                        if(data!=" "):
                            nearby_txt.append(data)
                    except Exception:
                        pass
                if (len(fd_train)>0):
                    X_Text=text_vectorizer.transform(nearby_txt).toarray()
                    result1=(clf2.predict(X_Text).reshape(1,-1))
                    result_prob = clf2.predict_proba(X_Text)
                    c=0
                    while c<len(result1[0]):
                        if result1[0][c]==1:
                            case= self.extract_case_number(data[c])
                            if case!="":
                                case1+=case+" "
                                #print str(max(result_prob[c])),"confidence for model"
                                scr+=str(max(result_prob[c]))+" "
                        c+=1
            if case1.strip()=="":
                Xtest = vect1.transform(data_line)
                result_line = Model1.predict(Xtest)
                scr_line= Model1.predict_proba(Xtest)
                c=0
                while c<len(data_line):
                    if result_line[c]==1 :
                        if data_line[c].find("c a6")>=0:
                            data_line[c]=""
                        case= self.extract_case_number(data_line[c])
                        if case!="":
                            case1+=case+" "
                            scr+=str(max(scr_line[c]))+" "
                    c+=1
            if case1.strip()=="":
                c=0
                while c<len(data_line):
                    if result_line[c]==1:
                        case= self.extract_case_number(' '.join(data_line[c-2:c+2]))
                        if case!="":
                            case1+=case+" "
                            scr+=str(max(scr_line[c]))+" "
                    c+=1
            if len(case1.split())==0 :
                case1 = "NONE"
                scr="0 "
            result_numbers =  list(set(case1.split()))
            scr_set=list(set(scr.split()))
            case_number=str(','.join(result_numbers))
            cs1=float(max(scr_set))
            data = {"esop_id": self.esop_id, "casenumber": case_number, "casenumber_cs": cs1}
            data_final = json.dumps(data)
            logger.info("sent result from casenumber "+ str(self.esop_id))
            return data_final
        
        else:
            data = {"esop_id": self.esop_id, "casenumber": None, "casenumber_cs": 0.0}
            data_final = json.dumps(data)
            logger.info("sent result from casenumber(else) "+ str(self.esop_id))
            return data_final
      except Exception,e:
        logger.info("exception from case number " +str(e)+ str(self.esop_id))
        error_handler = Error_Handler.Error_Handler()
        error_handler.mysql_insert_error("CaseNumber",myconfig.error_code2,str(self.esop_id)+" "+str(e))
        
        

        
   