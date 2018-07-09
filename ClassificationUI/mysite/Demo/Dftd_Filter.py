import numpy as np
from sklearn.externals import joblib
import myconfig
clf_filter=joblib.load(myconfig.dftd_filter_RF)
text_filter=joblib.load(myconfig.dftd_filter_text)
top_filter=joblib.load(myconfig.dftd_filter_top)
below_filter=joblib.load(myconfig.dftd_filer_below)
def filter_prediction(txt,top,below,X_tags):
    X_text=text_filter.transform([txt]).toarray()
    X_top=top_filter.transform([top]).toarray()
    X_below=below_filter.transform([below]).toarray()
    X_tags=[X_tags]
    X=[]
    for x1,x2,x3,x4 in zip(X_text,X_top,X_below,X_tags):
        tmp=[]
        for x in x1:
            tmp.append(x)
        for x in x2:
            tmp.append(x)
        for x in x3:
            tmp.append(x)
        for x in x4:
            tmp.append(x)
        X.append(tmp)
    X=np.asarray(X)
    return (int(clf_filter.predict(X)[0]))

