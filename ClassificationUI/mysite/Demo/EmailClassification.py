from .emlprocessing import EML
from sklearn.externals import joblib
import re
import os
from django.conf import settings

class EMLPrediction(EML):

    #clf = joblib.load(os.path.join(settings.MODEL_ROOT,"ClassifierRF.pkl"))
    #tfidf_body = joblib.load(os.path.join(settings.MODEL_ROOT,"body.pkl"))
    #tfidf_subject = joblib.load(os.path.join(settings.MODEL_ROOT,"subject.pkl"))

    def __init__(self):
        super().__init__()
        self.Y=None
        self.X=None
    def prediction(self,name):
        super().parse_eml(name)
        temp = self.body
        self.body=re.sub(' +',' ',re.sub('[^a-z0-9A-Z ]',' ',self.body))
        self.X=list(EMLPrediction.tfidf_body.transform([self.body]).toarray()[0])+\
               list(EMLPrediction.tfidf_subject.transform([self.subject]).toarray()[0])
        self.Y=EMLPrediction.clf.predict(self.X)
        if(self.Y[0]==1):
            result = "BA Map"
        elif(self.Y[0]==2):
            result = "ETD Setting"
        elif(self.Y[0]==3):
            result = "BAPLIE"
        elif(self.Y[0]==4):
            result = "CCH"
        else:
            result = "***"

        return (self.from_,self.to,temp.replace("\n","<br>"),self.subject,self.Y[0])
if __name__=='__main__':
    result=EMLPrediction().prediction('./Dataset/3.eml')
    print(result)
