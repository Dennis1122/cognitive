import difflib
import re
from party_title import plaintiff_party_title as ppt
from formatter import format_name
from taxpayers import handleTaxpayer,appendToList
def final_cleaning(temp):
    words_to_replace=['Claimant/Applicant','Claimant / Applicant','PLAINTIFF(S)/PETITIONER',\
                      'PLAINTIFF(S) /PETITIONER','PLAINTIFF(S)/ PETITIONER','PLAINTIFF(S) / PETITIONER',\
                      'PLAINTIFF(S)/PETITIONER','Plaintiff(s)','Plaintiffs','Plaintiff',\
                      'PLAINTIFF','Petitioner','PETITIONER',\
                      'Employee','Employees','EMPLOYEE','Debtor','Custodial',\
                      'Party','Insured','Claimant','Judgement', 'Creditor','CREDITOR(S)','Custodial',\
                      'Party','Pltf./Petitioner',\
                      'Plaintiffs Attorney','Applicant','claimant','CASE NAME:',\
                     'Employer','Insurance Carrier','Defendant','Employer','Insurance Carrier','RESPONDENT','DEFENDANT(s)/RESPONDENT:','DEFENDANT/RESPONDENTS:','DEFENDANT/RESPONDENTS','DEFENDANTS/RESPONDENTS','DEFENDANT / RESPONDENT','DEFENDANT /RESPONDENT','DEFENDANT/ RESPONDENT:','DEFENDANT / RESPONDENT:','Defendant/Respondent:','Defendant', 'Defendant/Respondent', 'Defendant(s)/Respondent',  'Defendant(s)/Respondent:',   'Defendants/Respondent:',    'Defendants/Respondents:','Defendant(S).','Defendant,','Defendants','Defendants,','Defendant.','Defendant','DEFENDANT','Respondent(s):','Respondents','Respondent','RESPONDENT','Employer:','Employers','Employers,','Employer,','EMPLOYER','Judgement Debtor','Obligor','CIRCUIT COURT STATE OF WISCONSIN','STATE OF WISCONSIN','WHEREFORE']
    for keywords in words_to_replace:
        temp = temp.replace(keywords,' ')
    words_to_rstrip=['The Property To Be Levied','P.O.',' St. ']
    for keywords in words_to_rstrip:
        if temp.upper().find(keywords.upper())>0:
            temp=temp[:temp.upper().find(keywords.upper())]
    words_to_lstrip=['Address Judgment Debtor','Debtor',' Address']
    for keywords in words_to_lstrip:
        if temp.upper().find(keywords.upper())>=0:
            temp=temp[temp.upper().find(keywords.upper()) + len(keywords):]
    return temp
def clean_text(txt):
    original_txt=txt
    import re
    txt=u''.join(txt).encode('utf-8').strip()
    regex = re.compile('[^a-zA-Z0-9-.?!,":\';()|\&/ ]')
    data = regex.sub(' ', txt)
    data = data.replace("\xc2\xa0"," ")
    data=re.sub(' +',' ',data)
    if data.find('section 374.240, RSMo 2000.')>0:
        data=data[data.find('section 374.240, RSMo 2000.')+len('section 374.240, RSMo 2000.'):]
    txt=data.split(' ')
    data=""
    for word,c in zip(txt,range(len(txt))):
        flag=False
        andFlag=True
        tmp = re.sub('[^a-zA-Z]','',word)
        for v in['vs','v','versus','against']:
            if tmp.lower().find(v)>=0 and len(tmp)<=len(v):
                data=data+"<versus>"+" "
                flag=True
                break
        if tmp.lower().find('and')>=0 and len(tmp)==3:
            for endWords in [' inc',' co','company']:
                try:
                    if original_txt.lower().split(' and ')[0].find(endWords) <=0 and original_txt.lower().split(' and ')[1].find(endWords)>0:
                        flag=False
                        andFlag=False
                        break
                except Exception as e:
                    flag=False
                    andFlag=False
                    break
                    pass
            if andFlag:
                if c<len(txt)-1:
                    next_word= re.sub('[^a-zA-Z]','',txt[c+1])
                    if next_word!=None:
                        if len(next_word)>=3 and (next_word.isupper() or next_word[0].isupper() or next_word.find('his')>=0):
                            data=data+"<and>"+" "
                            flag=True
        if not flag:
            data+=word
            data+=" "
    data = re.sub(' +',' ',data)
    return data
def searchforcolon(txt):
    loc=0
    keywords=['Re:','RESPONDING PARTY:','YOU ARE BEING SUED BY PLAINTIFF:','Petitioner(s):',\
              'PLAINTIFF/PETITIONER:','Regarding:','Petitioner(s):','WHEREFORE, the Plaintiffs;',"Plaintiff's Name","Defendant's Name",'Case Name:','Name And Address (Judgment Creditor)','Name And Address Judgment Debtor','Judgment Debtor Name']
    words=txt.split(' ')
    flag=False
    loc=0
    for word in keywords:
        if txt.lower().find(word.lower())>=0:
            loc=txt.lower().find(word.lower())+len(word)
    if loc == 0 and txt.find(':')>=0 and txt.find(':')<5:
        loc=txt.find(':')+1
    return txt[loc:].strip()
def  identify_description(pltf):
    #print "Pltf in identify_ description",pltf
    starts_with=[]
    ends_with=[]
    beginning =len(pltf)
    ending=-1
    patterns_etc=[' individually and ... deceased ',\
                  ' as special ... deceased ',' as the special ... deceased '
                  ' AS SUCCSSOR IN INTEREST TO ',' as assignee ',' assignee of ',' a/a/o '\
              ,' personal representatives for ',' as executor of ... deceased ',\
                  ' executrix of the estate of ... deceased ',' as the surviving heir ... deceased '\
                 ' individually and as successor in interest to ... deceased ',' as personal ',]

    for pattern in patterns_etc:
        if pattern.find('...')>=0:
            starts_with.append(pattern.split('...')[0])
            ends_with.append(pattern.split('...')[1])
        else:
            starts_with.append(pattern)
            ends_with.append(None)
        description_flag=False
    for start,end in zip(starts_with,ends_with):
        start=start.upper()
        if end!=None:
            end=end.upper()
        if pltf.upper().find(start.upper())>=0 and pltf.upper().find(start.upper()) < beginning:
            description_flag=True
            beginning=pltf.upper().find(start.upper())
            if end != None and pltf.upper().find(end)>=0 and pltf.upper().find(end) > end:
                ending=pltf.upper().find(end)+len(end)
            else:
                ending=len(pltf)-1
           
        else:
            continue
    
        
    if description_flag:
        name=pltf[:beginning]
        description=pltf[beginning:ending+1]
    else:
        name=pltf
        description=""
    return (name,description,description_flag)
def identify_etc(pltf):
    pltf=pltf.replace('spouse','wife')
    starts_with=[]
    ends_with=[]
    beginning =len(pltf)
    ending=-1
    words_to_strip=[' c/o ',' do ','demand']
    loc=-1
    for word in words_to_strip:
        if pltf.find(word)>=0:
            pltf=pltf[:pltf.find(word)]
            break
    if pltf.find('his wife')<=3 and pltf.find('his wife')>=0:
        beginning=pltf.find('his wife')+len('his wife')+1
        end = -1
        name=pltf[beginning:].strip()
        description='etc'
        description_flag=True
    else:
        patterns_etc=[' NOT IN ',' her husband',' his wife','d/b/a',' As ... Fiscal ',' A CORPORATION ',' an individual',' AS ',' dba ',\
                      ' f/k/a',' fka ',' FICA ','unknown','successor','aka','a/k/a','as assignee','d/bla','receiver',' as ',\
                     ' a business entity',', A ',' assignee ',' issuer ',' husband',' An ',', An ']
        for pattern in patterns_etc:
            if pattern.find('...')>=0:
                starts_with.append(pattern.split('...')[0])
                ends_with.append(pattern.split('...')[1])
            else:
                starts_with.append(pattern)
                ends_with.append(None)
            description_flag=False
        for start,end in zip(starts_with,ends_with):
            start=start.upper()
            if end!=None:
                end=end.upper()
            if pltf.upper().find(start.upper())>=0 and pltf.upper().find(start.upper()) < beginning:
                description_flag=True
                beginning=pltf.upper().find(start.upper())
                if end != None and pltf.upper().find(end)>=0 and pltf.upper().find(end) > end:
                    ending=pltf.upper().find(end)+len(end)
                else:
                    ending=len(pltf)-1

            else:
                continue
        if pltf.find(' a ')< beginning and pltf.find(' a ') >=4:
            description_flag=True
            beginning = pltf.find(' a ')
            ending = len(pltf)-1
        
        if description_flag:
            name=pltf[:beginning]
            description='etc'
        else:
            name=pltf
            description=""
    return (name,description,description_flag)


def extract_involuntary(involuntary):
    import difflib
    for names in involuntary:
        pltfs=[]
        names=names.split(' ')
        c=1
        word = ""
        i=0
        for name,l in zip(names,range(len(names))):
            if name.find(',')>=0 or name.find(';')>=0 or name.upper().find('INC')>=0 or name.upper().find('LLC')>=0:
                if l<len(names)-1:
                    if names[l+1].find('INC')>=0 or names[l+1].find('LLC')>=0:
                        word = word + name+" "+names[l+1]+" "
                        c+=1
                        
                    else :
                        if c <2:
                            word = word + name+" "
                            c+=1
                        else:
                            word = word + name+" "
                            flag = False
                            for i in range(len(pltfs)):
                                if difflib.SequenceMatcher(None,pltfs[i].lower(),word.lower()).ratio()*100 > 80:
                                    flag=True
                                    if len(pltfs[i])< len(word):
                                        pltfs[i]=word
                                        word=""
                                        break  
                            if len(pltfs)==0:
                                pltfs.append(word.strip())
                            elif not flag:
                                pltfs.append(word.strip())
                            word = ""
                            c=0
            else:
                word = word+ name+ " "
                c+=1
            i+=1
    if len(pltfs)==0:
        return None
    elif len(pltfs)==1:
        return pltfs[0].strip(',').strip()+', '+'Involuntary Pltf'
    elif len(pltfs)==2:
        return pltfs[0].strip(',').strip()+' and '+pltfs[1].strip(',').strip()+' Involuntary Pltfs '
    else :
        return pltfs[0].strip(',').strip()+', et al., '+'Involuntary Pltfs'

def clean_result(temp):
    import re
    regex = re.compile('[^a-zA-Z0-9-.?!,\"\:\';()|\&/ ]')
    temp = regex.sub(' ', temp)
    if temp.find(' et al ') >=0:
        temp=temp[:temp.find(' et al ')].strip()
    temp=re.sub(' +',' ',temp)
    words=temp.split()
    temp=""
    i=0
    for word in words:
        if re.search('\d',word) and i!=0 and len(re.sub('[^a-zA-Z]','',word))==0:
            
            if re.search('\d',word).start()==0:
                break
        i+=1
        temp=temp+word+" "
    if temp.find('(')>=0 and temp.find(')')>=0:
        pass
    else:
        temp = temp.replace('(','')
        temp= temp.replace(')','')
    return temp.strip()
def extractor_plaintiff(pltfs,pltf_details,involuntary):
    Plaintiff=[]
    Plaintiff_level2=[]
    Plaintiff_level3=[]
    Plaintiff_Final=[]
    Plaintiff_description=[]
    Defendant=[]
    etc=[]
    description=[]
    pltf_tmp=[]
    for pltf in pltfs:
        pltf=clean_text(pltf) 
        if pltf.find('<versus>')>=0:
            level1=pltf.split('<versus>')[0]
        else:
            level1=pltf
        if level1.find('<and>')>=0:
            pos=level1.find('<and>')
            if  not level1[pos+6:].split(' ')[0].islower() or level1[pos+6:].split(' ')[0].find('his')  or level1[pos+6:].split(' ')[0].find('her')>=0:
                for name in level1.split('<and>'):
                    flag=False
                    for i in range(len(pltf_tmp)):
                        if difflib.SequenceMatcher(None,pltf_tmp[i].lower(),name.lower()).ratio()*100 > 80:
                            flag=True
                            if len(pltf_tmp[i])< len(name):
                                pltf_tmp[i]=name.strip()
                                #print "Appended1:",name
                    if not flag : 
                        pltf_tmp.append(name.strip())
                        #print "Appended2:",name
                    if len(pltf_tmp)==0:
                        pltf_tmp.append(name.strip())
                        #print "Appended3:",name
            else:
                name=level1
                #print name
                for i in range(len(pltf_tmp)):
                        if difflib.SequenceMatcher(None,pltf_tmp[i].lower(),name.lower()).ratio()*100 > 80:
                            if len(pltf_tmp[i])< len(name):
                                pltf_tmp[i]=name
                if len(pltf_tmp)==0:
                    pltf_tmp.append(name.strip())
                    #print "Appended4",name

        else:
            name=level1
            #print name
            flag=False
            for i in range(len(pltf_tmp)):
                if difflib.SequenceMatcher(None,pltf_tmp[i].lower(),name.lower()).ratio()*100 > 80:
                    flag=True
                    if len(pltf_tmp[i])< len(name):
                        pltf_tmp[i]=name
            if not flag:
                pltf_tmp.append(name.strip())
            if len(pltf_tmp)==0:
                pltf_tmp.append(name.strip())
                #print "Appended4",name
            #print "Appended5:",level1
    #print "\n\nPlaintiffs Level 1 "
    for tmp in pltf_tmp:
        #print tmp
        name = searchforcolon(tmp)
        flag=False
        for i in range(len(Plaintiff_level2)):
            #print name,Plaintiff[i],difflib.SequenceMatcher(None,Plaintiff[i].lower(),name.lower()).ratio()*100
            if difflib.SequenceMatcher(None,Plaintiff_level2[i].lower(),name.lower()).ratio()*100 > 80:
                flag=True
                break
        if not flag:
            Plaintiff_level2.append(name)
        if len(Plaintiff_level2)==0:
            Plaintiff_level2.append(name)


    #print "\n\nPlaintiff Level2"
    for pltf in Plaintiff_level2:
        #print pltf #pass
        result = identify_description(pltf)
        #print result
        if result[2]:
            temp=clean_result(result[0]) 
            desc=clean_result(result[1])
        else:
            result = identify_etc(pltf)
            temp=clean_result(result[0]) 
            desc=clean_result(result[1]) 
        flag=False
        temp=final_cleaning(temp)
        for i in range(len(Plaintiff_Final)):
            #print name,Plaintiff[i],difflib.SequenceMatcher(None,Plaintiff[i].lower(),name.lower()).ratio()*100
            if difflib.SequenceMatcher(None,Plaintiff_Final[i].lower(),temp.lower()).ratio()*100 > 80:
                flag=True
                if len(Plaintiff_Final[i])<temp:
                    Plaintiff_Final[i]=temp
                break
        if not flag and len(re.sub('[^a-zA-Z]','',temp))>=3:
            Plaintiff_Final.append(temp)
            Plaintiff_description.append(desc)
        if len(Plaintiff_Final)==0 and len(re.sub('[^a-zA-Z]','',temp)):
            Plaintiff_Final.append(temp)
            Plaintiff_description.append(desc)
    party_title=ppt(pltf_details)
    if party_title.lower().find('plaintiff')>=0 or party_title.find('None')>=0 or party_title==None:
        party_title='Pltf'
    return  format_name(Plaintiff_Final,Plaintiff_description,party_title)
def extractor_defendant(dftds,details):
    from party_title import defentant_party_title as dpt
    Defendant=[]
    Defendant_level2=[]
    Defendant_level3=[]
    Defendant_Final=[]
    Defendant_description=[]
    Defendant=[]
    etc=[]
    description=[]
    dftd_tmp=[]
    for dftd in dftds:
        dftd=clean_text(dftd)
        if dftd.find('<versus>')>=0:
            level1=dftd.split('<versus>')[1]
        else:
            level1=dftd
        if level1.find('<and>')>=0:
            pos=level1.find('<and>')
            if  not level1[pos+6:].split(' ')[0].islower() or level1[pos+6:].split(' ')[0].find('his') or level1[pos+6:].split(' ')[0].find('her')>=0:
                for name in level1.split('<and>'):
                    flag=False
                    for i in range(len(dftd_tmp)):
                        if difflib.SequenceMatcher(None,dftd_tmp[i].lower(),name.lower()).ratio()*100 > 80:
                            flag=True
                            if len(dftd_tmp[i])< len(name):
                                dftd_tmp[i]=name.strip()
                                #print "Appended1:",name
                    if not flag : 
                        dftd_tmp.append(name.strip())
                        #print "Appended2:",name
                    if len(dftd_tmp)==0:
                        dftd_tmp.append(name.strip())
                        #print "Appended3:",name
            else:
                name=level1
               
                for i in range(len(dftd_tmp)):
                        if difflib.SequenceMatcher(None,dftd_tmp[i].lower(),name.lower()).ratio()*100 > 80:
                            if len(dftd_tmp[i])< len(name):
                                dftd_tmp[i]=name
                if len(dftd_tmp)==0:
                    dftd_tmp.append(name.strip())
                    
        elif level1.lower().find('taxpayer')>=0:
            names=handleTaxpayer(level1)
            for name in names:
                dftd_tmp=appendToList(dftd_tmp,name)
        else:
            name=level1
            #print name
            flag=False
            for i in range(len(dftd_tmp)):
                if difflib.SequenceMatcher(None,dftd_tmp[i].lower(),name.lower()).ratio()*100 > 80:
                    flag=True
                    if len(dftd_tmp[i])< len(name):
                        dftd_tmp[i]=name
            if not flag:
                dftd_tmp.append(name.strip())
            if len(dftd_tmp)==0:
                dftd_tmp.append(name.strip())
        #print "Defendant Temp",dftd_tmp
    for tmp in dftd_tmp:
        #print tmp
        name = searchforcolon(tmp)
        flag=False
        for i in range(len(Defendant_level2)):
            #print name,Defendant[i],difflib.SequenceMatcher(None,Defendant[i].lower(),name.lower()).ratio()*100
            if difflib.SequenceMatcher(None,Defendant_level2[i].lower(),name.lower()).ratio()*100 > 80:
                flag=True
                break
        if not flag:
            Defendant_level2.append(name)
        if len(Defendant_level2)==0:
            Defendant_level2.append(name)
    


    #print "\n\nDefendant Level2"
    for dftd in Defendant_level2:
        #print dftd #pass
        result = list(identify_description(dftd))
        if len(result[1])>0:
            result[1]='etc'
        #print result
        if result[2]:
            temp=clean_result(result[0]) 
            desc=clean_result(result[1])
        else:
            result = identify_etc(dftd)
            temp=clean_result(result[0]) 
            desc=clean_result(result[1]) 
        flag=False
        temp=final_cleaning(temp)
        for i in range(len(Defendant_Final)):
            #print name,Defendant[i],difflib.SequenceMatcher(None,Defendant[i].lower(),name.lower()).ratio()*100
            if difflib.SequenceMatcher(None,Defendant_Final[i].lower(),temp.lower()).ratio()*100 > 80:
                flag=True
                if len(Defendant_Final[i])<temp:
                    Defendant_Final[i]=temp
                break
        if not flag and len(re.sub('[^a-zA-Z]','',temp))>=3:
            Defendant_Final.append(temp)
            Defendant_description.append(desc)
        if len(Defendant_Final)==0 and len(re.sub('[^a-zA-Z]','',temp)):
            Defendant_Final.append(temp)
            Defendant_description.append(desc)
    party_title=dpt(details)
    if party_title.lower().find('defend')>=0 or party_title.lower() =='none':
        party_title='Dft'
    return format_name(Defendant_Final,Defendant_description,party_title)