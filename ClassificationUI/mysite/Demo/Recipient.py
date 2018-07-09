from sklearn.externals import joblib
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import sent_tokenize
def get_sender(data):
    sender=''
    greetings = ["regards","Thanks in advance","Regards","Thanks",\
                 "Thank you","Thx","Thansk","thank you very much","Many thanks",'Cheers']
    last = ' '.join(data.split(" ")[-5:])
    for j in greetings:
        if last.lower().find(j.lower())>=0:
            foundat = last.lower().find(j.lower())
            sender = last[foundat+len(j):]
            sender = sender.strip(' ')
            sender = sender.strip(',')
            sender = sender.strip('.')
            sender = sender.strip(' ')
            break
    return sender
def cleaning_text(text):
    abbreviations={' RM ':' regional manager ',' RE ':' regional executive ',' RM-':' regional manager '\
                   ,' BM ':' manager ' }
    for key in abbreviations.keys():
        text = text.replace(key,abbreviations[key])
    p = re.compile(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+', re.MULTILINE | re.IGNORECASE)
    mailId=re.findall(p,text)
    for mail in mailId:
        name=mail.split('@')[0].replace('.',' ').replace('"','')
        name=[a[0].upper()+a[1:].lower() for a in name.split(' ')]
        name=u' '.join(name)
        text = text.replace(mail,name)
    regex = re.compile('[^a-zA-Z0-9.?!,\';|\& ]')
    text = regex.sub('', text)
    text = re.sub(' +',' ',text)
    return text
def traverse_tree(tree,words,tags):
    if type(tree)==tuple:
        return (words.append(tree[0]),tags.append(tree[1]))
    else:
        for node in tree:
            traverse_tree(node,words,tags)
        return (words,tags)
def get_recipient(processNotes):
    stop_words = set(stopwords.words('english'))
    stop_words.remove('me')
    stop_words.add('docs')
    stop_words.add('mail')
    stop_words|=set(['NO','Frahins', 'Attn','EMAIL','EMU','BBC', 'CREK','ATT','ATTN','TPG', 'SOUTH', 'JOHNSTONE','MyOrganisastion', 'ANDROMACHE', 'Manager','EBT', 'NOTE', 'OTHER', 'PART', 'THIS', 'HAS', 'BEEN', 'CHECKED', \
                     'BY', 'ME', 'APART', 'FROM', 'THE', 'TRUST', 'ADVISING',\
                     'Company','security', 'settlement', 'management', 'preparation', 'documents', 'signing'])
    trim_words = ['Thank', 'Kind', 'Regards', 'Cheers']
    words_to_exclude = ['Banker', 'BSB', 'Lync', 'CDL', 'Checklist', 'Please', 'Are', 'Account', 'Number', \
                        'CGE', 'Product', 'Marked', 'Can', 'ASAP', 'Monday', 'Sunday', 'Tuesday', 'Wednesday',
                        'Thursday' \
        , 'Friday', 'Saturday', 'January', 'February', 'March', 'April', 'May',\
                        'June', 'July', 'August', \
                        'September', 'October', 'November', 'December', 'Branch',\
                        'PO', 'Box', 'DGT', 'SSW']
    nearby_words_to_look = ['attention', 'send', 'sent', 'email', 'mail']
    words_as_client = ['client', 'clients', 'company']
    words_as_sender = ['branch', 'office']
    clf=joblib.load('/home/1127263/Experiments/Django/mysite/Demo/Models/RFRecipient.pkl')
    tfidf=joblib.load('/home/1127263/Experiments/Django/mysite/Demo/Models/TFIDFRecipient.pkl')
    note = cleaning_text(processNotes)
    X = []
    for sentence in sent_tokenize(note):
        X.append(sentence)
    results=clf.predict(tfidf.transform(X))
    inputs=[X[i] for i in range(len(X)) if results[i]==1]
    if len(inputs)==0:
        print("No sender not available")
        return None

    recipient_flag = False
    for txt in inputs:
        for a in trim_words:
            if txt.find(a) > 0:
                txt = txt[:txt.find(a)]
        tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(txt)))
        words, tags = (traverse_tree(tree, [], []))
        index = [i for i in range(len(tags)) if tags[i] == 'TO']
        if len(index) == 0:
            recipient = get_sender(note)
            continue
        else:
            recipient = ''
            index = index[0]
        words = words[index + 1:]
        tags = tags[index + 1:]
        NNP = [words[i] for i in range(len(tags)) if tags[i] == 'NNP' and \
               words[i] not in stop_words and words[i] not in words_to_exclude]
        NN = [words[i] for i in range(len(tags)) if
              (tags[i] == 'NN' or tags[i] == 'NNS') and words[i] not in stop_words]
        PRP = [words[i] for i in range(len(tags)) if tags[i] == 'PRP']
        recipient_flag = False
        for word in words_as_client:
            if word in NN:
                return('ENRICH client name')
                recipient_flag = True
        for word in words_as_sender:
            if word in NN:
                return (get_sender(note))
                recipient_flag = True
        if len(NNP) > 0 and not recipient_flag:
            i = 0
            while i < len(NNP) and i < 2:
                recipient += NNP[i] + ' '
                if NNP[i] == 'BU':
                    break
                i += 1
            return(recipient)
        elif not recipient_flag and len(PRP) > 0:
            return(get_sender(note))
        elif not recipient_flag and len(NN) > 0:
            i = 0
            while i < len(NN) and i < 2:
                recipient += NN[i] + ' '
                i += 1
            return(recipient)
        elif not recipient_flag:
            return(get_sender(note))
    return recipient
"""if __name__=='__main__':
    df = pd.read_csv('./Dataset.csv', usecols=['Process Notes'])
    df1 = pd.read_csv('./Dataset2.csv', usecols=['Process Notes'])
    df=df.append(df1)
    processNotes = [cleaning_text(x) for x in list(df['Process Notes'])]
    i=1
    for note in processNotes:
        print(i)
        print('Process note ==> ', note)
        recipient = get_recipient(note)
        if recipient=='':
            recipient='Commentator'
        print('Recipient Name ==> ', recipient)
        i+=1"""