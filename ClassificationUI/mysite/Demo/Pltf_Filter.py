import numpy as np
from sklearn.externals import joblib
import myconfig
clf_filter=joblib.load(myconfig.pltf_filter_RF)
text_filter=joblib.load(myconfig.pltf_filter_text)
top_filter=joblib.load(myconfig.pltf_filter_top)
below_filter=joblib.load(myconfig.pltf_filer_below)
def filter_prediction(txt,top,below):
    X_text=text_filter.transform([txt]).toarray()
    X_top=top_filter.transform([top]).toarray()
    X_below=below_filter.transform([below]).toarray()
    X=[]
    for x1,x2,x3 in zip(X_text,X_top,X_below):
        tmp=[]
        for x in x1:
            tmp.append(x)
        for x in x2:
            tmp.append(x)
        for x in x3:
            tmp.append(x)
        X.append(tmp)
    X=np.asarray(X)
    return (int(clf_filter.predict(X)[0]))

