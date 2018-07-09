import difflib
from nltk.tokenize import word_tokenize
def handle_taxpayer(result):
    txt=result[result.lower().find('taxpayer ')+9:]
    tokens=word_tokenize(txt)
    name=""
    used=[]
    names=[]
    skip=0
    for token in tokens:
        i=0
        while i < skip:
            i+=1
            continue
        skip=0
        if token not in used:
            #name = name+token+" "
            used.append(token)
        else:
            name=""
            for k in used:
                name=name+k+" "
            skip=len(used)
            if len(name)>2:
                #print name
                names=appendToList(names,name)
                name=""
                used=[]
                used.append(token)
        if token.lower()=='inc' or token.lower()=='inc.':
            for k in used:
                name=name+k+" "
            #print name
            names=appendToList(names,name)
            name=""
            used=[]
    for k  in used:
        name=name+k+" "
    if len(name)>0:
        #print name
        names=appendToList(names,name)
    return names
def appendToList(lst,name,score=50):
    flag=False
    for i in range(len(lst)):
        if difflib.SequenceMatcher(None,lst[i].lower(),name.lower()).ratio()*100>score:
            flag=True
            if len(lst[i])<len(name):
                lst[i]=name
            break
    if not flag:
        lst.append(name)
    return lst
def handleTaxpayer(result):
    import re
    result=re.sub(' +',' ',result)
    txt=result[result.lower().rfind('taxpayer')+9:]
    tokens=txt.split(' ')
    i=0
    temp=[]
    names=[]
    while i < len(tokens):
        if tokens[i] not in temp:
            temp.append(tokens[i])
            i+=1
        else:
            skip = len(temp)
            i+=skip
            #print temp
            name=""
            for k in temp:
                name=name+k+" "
            name=name.strip()
            if len(name)>2:
                names=appendToList(names,name,60)
            temp=[]
            continue
        if tokens[i-1].lower().find('inc')==0:
            name=""
            for k in temp:
                name=name+k+" "
            name=name.strip()
            if len(name)>2:
                names=appendToList(names,name,60)
            temp=[]
    if len(temp)>0:
        name=""
        for k in temp:
            name=name+k+" "
        name=name.strip()
        if len(name)>2:
                names=appendToList(names,name,60)
    return names
