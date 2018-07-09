def prediction(text,top,below,clf,text_vectorizer_pltf,               top_vectorizer_pltf,below_vectorizer_pltf,              text_vectorizer_dftd,top_vectorizer_dftd,below_vectorizer_dftd,               text_vectorizer_zero,top_vectorizer_zero,below_vectorizer_zero):
    from POSTagging import find_pos_tags
    X=[]
    x4=find_pos_tags(text)
    top_tags=find_pos_tags(top)
    below_tags=find_pos_tags(below)
    for xp1,xp2,xp3,xd1,xd2,xd3,xz1,xz2,xz3 in     zip(text_vectorizer_pltf.transform(text).toarray(),        top_vectorizer_pltf.transform(top).toarray(),        below_vectorizer_pltf.transform(below).toarray(),        text_vectorizer_dftd.transform(text).toarray(),        top_vectorizer_dftd.transform(top).toarray(),        below_vectorizer_dftd.transform(below).toarray(),       text_vectorizer_zero.transform(text).toarray(),        top_vectorizer_zero.transform(top).toarray(),        below_vectorizer_zero.transform(below).toarray()):
        tmp=[]
        for x in xp1:
            tmp.append(x)
        for x in xp2:
            tmp.append(x)
        for x in xp3:
            tmp.append(x)
        for x in x4:
            tmp.append(x)
        for x in xd1:
            tmp.append(x)
        for x in xd2:
            tmp.append(x)
        for x in xd3:
            tmp.append(x)
        for x in xz1:
            tmp.append(x)
        for x in xz2:
            tmp.append(x)
        for x in xz3:
            tmp.append(x)
        X.append(tmp)
    return (int(clf.predict(X)[0]),max(clf.predict_proba(X)),X)

