import re
from StringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import os
from nltk.corpus import stopwords
from sklearn.externals import joblib
import pickle
import json
import myconfig
from loger import logger
import Error_Handler


vectorizer = pickle.load(open(myconfig.attachment_feature_path, "rb"))
model = joblib.load(myconfig.attachment_model_path)

class Attachment:

    def __init__(self, esop_id, pdf_read):
        self.stop = set(stopwords.words('english'))
        self.esop_id = esop_id
        self.pdf_read = pdf_read


    def textextractor(self, path, pages=None):
        all_pages = []
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        manager = PDFResourceManager()
        fd = open(path, 'rb')
        for page in PDFPage.get_pages(fd, pagenums):
            output = StringIO()
            converter = TextConverter(manager, output, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, converter)
            interpreter.process_page(page)
            all_pages.append(output.getvalue())

            converter.close()
            output.close()
        fd.close()
        return all_pages

    def clean_text(self, data):
        data = data.lower()
        data = data.replace("\xc2\xa0", " ")
        data = data.replace("\n\n\n", " ")
        data = data.replace("\n\n", " ")
        data = data.replace("\n", " ")
        regex = re.compile('[^a-zA-Z, ]')
        data = regex.sub('', data)
        data = re.sub(' +', ' ', data)
        data = ' '.join(i for i in data.lower().split() if i not in self.stop)
        return data

    def predict(self):
      try:
        logger.info("starting attachment prediction for esop " + str(self.esop_id))
        document_pages = self.pdf_read
        cleaned_pages = []
        for page in document_pages:
            cleaned_pages.append(self.clean_text(page))

        x_test_vector = vectorizer.transform(cleaned_pages)

        predicted_result = model.predict(x_test_vector)
        c = model.predict_proba(x_test_vector)
        sum1 = 0
        count = 0
        for i in c:
            sum1 = sum1 + max(i)
            count = count + 1
        cs = sum1 / count

        result = list(set(predicted_result))
        attachment = '#'.join(result)
        result = {"esop_id": self.esop_id, "attachment": attachment, "attachment_cs": cs}
        result_final = json.dumps(result)
        logger.info("sent result from attachment "+ str(self.esop_id))
        return result_final
      except Exception,e:
        logger.info("exception from attachment " +str(e)+ str(self.esop_id))
        error_handler = Error_Handler.Error_Handler()
        error_handler.mysql_insert_error("Attachment",myconfig.error_code2,str(self.esop_id)+" "+str(e))