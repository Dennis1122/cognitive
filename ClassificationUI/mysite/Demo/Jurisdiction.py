import nltk
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from nltk import ngrams
from sklearn.externals import joblib
import pickle
import pdfquery
import json
import myconfig
from loger import logger
import Error_Handler
clf = joblib.load(myconfig.jurisdiction_model_path)
tf = pickle.load(open(myconfig.jurisdiction_feature_path, "rb"))
class Jurisdiction:
    def __init__(self, esop_id, pdf_readLine,pdf_readPage):
        self.F = []
        self.B = []
        self.J = []
        self.data = []
        self.esop_id = esop_id
        self.pdf_readPage = pdf_readPage
        self.pdf_readLine = pdf_readLine

    def pre_process(self, text):
        text = text.lower()
        text = text.replace("\n", " ")
        regex = re.compile('[0-9]+')
        text = regex.sub('numberblock', text)
        text = text.replace(',', 'commachar')
        text = text.replace('.', 'dotchar')
        text = text.replace(' c ', ' corporation ')
        text = text.replace('c ', 'corporation ')
        text = text.replace(' t ', ' trust ')
        text = text.replace(' c/o ', ' careof ')
        text = text.replace(' s/o ', ' careof ')
        text = text.replace(' c-o ', ' careof ')
        text = text.replace('c/o ', ' careof ')
        text = text.replace('c-o ', ' careof ')

        return text
    """ This pgm will read a pdf and will extract page and cordinate details of text present in the pdf file"""
    def pdf_reader(self, path):
        page_pos_dict = []
        pdf = pdfquery.PDFQuery(path)
        i = 0
        try:
            while i <= 7:
                pdf.load(i)
                jquery = pdf.pq('LTPage')
                if jquery.text().find('Service of Process Transmittal') >= 0:
                    i += 1
                    continue
                for j in jquery("LTTextBoxHorizontal"):
                    page_pos_dict.append(jquery(j).text())
                i += 1
        except Exception, e:
            logger.info(str(e))
            return page_pos_dict
        return page_pos_dict

    def clean_text(self, data):
        data = u''.join(data).encode('utf-8').strip()
        data = data.lower()
        data = data.replace("\xa0", " ")
        data = data.replace("0xa0", " ")
        data = data.replace("\xc2\xa0", " ")
        data = data.replace("\n\n\n", " ")
        data = data.replace("\n\n", " ")
        data = data.replace("\n", " ")
        regex = re.compile('[^a-zA-Z, ]')
        data = regex.sub(' ', data)
        data = re.sub(' +', ' ', data)
        data = ' '.join(i for i in data.lower().split())
        data = data.replace("ct log number", "ctlognumber")
        data = data.replace("ct corporation", "ctcorporation")
        data = data.replace("ct other", "ctother")
        data = data.replace("ct has", "cthas")
        data = data.replace("ct corp", "ctcorp")
        data = data.replace("ct contact", "ctcontact")
        return data

    def page_extractor(self, directory_files, pages=None):
        all_page_set = []
        global front_page
        front_page = []
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)
        try:
            path = directory_files
            manager = PDFResourceManager()
            fd = open(path, 'rb')
            page_no = 0
            f_page = ""
            all_pages = []
            for page in PDFPage.get_pages(fd, pagenums):
                output = StringIO()
                converter = TextConverter(manager, output, laparams=LAParams())
                interpreter = PDFPageInterpreter(manager, converter)
                interpreter.process_page(page)
                doc = output.getvalue()
                if doc[:18] == "Service of Process":
                    f_page = f_page + doc
                else:
                    page_no = page_no + 1
                    if page_no > 5:
                        front_page.append(f_page)
                        break
                    all_pages.append(doc)
                converter.close()
                output.close
            all_page_set.append(' '.join(all_pages))
            fd.close()
        except Exception, e:
            logger.info("exception from jurisdiction "+ str(self.esop_id)+str(e))
        return all_page_set

    def jurisdiction_suggestions(self, data):
        data = data.lower()
        regex = re.compile('[^a-zA-Z0-9,. ]')
        data = regex.sub(' ', data)
        data = re.sub(' +', ' ', data)

        regex = re.compile('[0-9]+')
        data = regex.sub('<num>', data)

        n = 4
        ngram_list = []
        grams = ngrams(data.split(), n)
        for gram in grams:
            ngram_list.append((' '.join(gram)))
        # print ngram_list

        suggetions = []

        for item in ngram_list:
            suggestions1 = re.findall("court of ([a-z ]+)", item)
            suggestions3 = re.findall("court of ([a-z ]+), county of", item)
            suggestions4 = re.findall("court of ([a-z ]+) county of", item)
            suggestions5 = re.findall("state of ([a-z ]+),", item)
            suggestions6 = re.findall("state of ([a-z ]+).", item)
            suggestions7 = re.findall("state of ([a-z ]+)", item)
            suggestions15 = re.findall("state of ([a-z]+)", item)
            suggestions8 = re.findall("county, ([a-z ]+)", item)
            suggestions9 = re.findall("code of ([a-z ]+)", item)
            suggestions10 = re.findall("commonwealth of ([a-z ]+)", item)
            suggestions11 = re.findall("council of ([a-z ]+),", item)
            suggestions12 = re.findall("district of ([a-z ]+),", item)
            suggestions13 = re.findall(", ([a-z ]+) <num>", item)
            suggestions14 = re.findall("(?<=\,).+?(?=\.)", item)

            sub_suggetions = suggestions15 + suggestions1 + suggestions3 + suggestions4 + suggestions5 + suggestions6 + suggestions7 + suggestions8 + suggestions9 + suggestions10 + suggestions11 + suggestions12 + suggestions13 + suggestions14

            # print sub_suggetions

            suggetions.append(sub_suggetions)
        flat_list = list(set([item.upper() for suggetion in suggetions for item in suggetion]))
        # print flat_list
        k = 0
        for item in flat_list:
            if item in myconfig.state_code_dictionary.values():
                return item
        if k != 1:
            for item in flat_list:
                if item in myconfig.state_code_dictionary.keys():
                    return myconfig.state_code_dictionary[item]

    def predict(self):
      try:
        logger.info("starting jurisdiction prediction for esop " + str(self.esop_id))
        global fd
        global data
        data = self.pdf_readLine
          
        #print self.path

        for x in data:
            block = self.pre_process(x)
            xd = tf.transform([block])
            result = clf.predict(xd)

            if result[0] == 1:
                cs = clf.predict_proba(xd)
                cs1 = max(max(cs))
                text = u''.join(x).encode('utf-8').strip()
                tokens = nltk.word_tokenize(x)
                for word in reversed(tokens):
                    if word in myconfig.state_code_dictionary.keys():
                        self.J.append(myconfig.state_code_dictionary[word])
                        self.B.append(text)
                        if myconfig.state_code_dictionary[word] == myconfig.connecticut:
                            docus = self.pdf_readPage
                            jurisdiction = self.jurisdiction_suggestions(docus[0])
                            data = {"esop_id": self.esop_id, "jurisdiction": jurisdiction, "jurisdiction_cs": cs1}
                            data_final = json.dumps(data)
                            logger.info("sent result from jurisdiction(case 1)"+ str(self.esop_id))
                            return data_final
                        else:
                            data = {"esop_id": self.esop_id, "jurisdiction": myconfig.state_code_dictionary[word],
                                    "jurisdiction_cs": cs1}
                            data_final = json.dumps(data)
                            logger.info("sent result from jurisdiction(case 2)"+ str(self.esop_id))
                            return data_final

        docus = self.pdf_readPage
        jurisdiction = self.jurisdiction_suggestions(docus[0])
        if jurisdiction != "":
          data = {"esop_id": self.esop_id, "jurisdiction": jurisdiction,
                "jurisdiction_cs": myconfig.cs_juri_specialcase}
          data_final = json.dumps(data)
        else:
          data = {"esop_id": self.esop_id, "jurisdiction": jurisdiction,
                "jurisdiction_cs": 0}
          data_final = json.dumps(data)
        logger.info("sent result from jurisdiction(case 3) "+ str(self.esop_id))
        return data_final
      except Exception,e:
        logger.info("exception from Jurisdiction " +str(e)+ str(self.esop_id))
        error_handler = Error_Handler.Error_Handler()
        msg = str(self.esop_id)+" "+str(e)
        error_handler.mysql_insert_error("Jurisdiction",myconfig.error_code2,msg)
