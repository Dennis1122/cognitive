import re
from pdfreader import read_pdf
from nltk.corpus import stopwords
from sklearn.externals import joblib
import json
import myconfig
from loger import logger
import warnings
import Error_Handler
tfidf = joblib.load(myconfig.lawsuit_feature_path)
classifier = joblib.load(myconfig.lawsuit_model_path)
class Lawsuit:

    def __init__(self, esop_id, pdf_read):
        self.esop_id = esop_id
        self.pdf_read = pdf_read

    def clean_text(self, document):
        stop_words = set(stopwords.words('english'))
        cleaned_data = ""
        for page in document:
            if page.lower().find("service of process") < 0:
                cleaned_data += page
        cleaned_data = cleaned_data.lower()
        cleaned_data = cleaned_data.replace("\xc2\xa0", " ")
        cleaned_data = cleaned_data.replace("\n\n\n", " ")
        cleaned_data = cleaned_data.replace("\n\n", " ")
        cleaned_data = cleaned_data.replace("\n", " ")
        regex = re.compile('[^a-zA-Z ]')
        cleaned_data = regex.sub(' ', cleaned_data)
        cleaned_data = re.sub(' +', ' ', cleaned_data)
        cleaned_data = ' '.join(word for word in cleaned_data.lower().split() if word not in stop_words)
        return cleaned_data

    def predict(self):
      try:
        logger.info("starting lawsuit prediction for esop "+str(self.esop_id))
        data = self.clean_text(self.pdf_read)
        with warnings.catch_warnings():
          warnings.simplefilter("ignore", category=UserWarning)
          x = tfidf.transform([data])
          lawsuit = classifier.predict(x)[0].strip()
          cs = max(max(classifier.predict_proba(x)))
          data = {"esop_id": self.esop_id, "lawsuit": lawsuit, "lawsuit_cs": cs}
          data_final = json.dumps(data)
          logger.info("sent result from lawsuit "+ str(self.esop_id))
          return data_final
      except Exception,e:
        logger.info("exception from Lawsuit " +str(e)+ str(self.esop_id))
        error_handler = Error_Handler.Error_Handler()
        error_handler.mysql_insert_error("Lawsuit",myconfig.error_code2,str(self.esop_id)+" "+str(e))
        
