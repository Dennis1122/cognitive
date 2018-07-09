import difflib
def clean(txt):
    txt = txt.lower()
    txt = txt.replace("#"," ")   
    return txt


def find_Ngrams(input_list,n):
    ngram_list = []
    for i in range(len(input_list)-n+1):
        ngram_list.append(' '.join(input_list[i:i+n]))
    return ngram_list


def plaintiff_party_title(name_list):
    plaintiff_keywords = ['Claimant/Applicant', 'Claimant / Applicant', 'PLAINTIFF(S)/PETITIONER', 'PLAINTIFF(S) /PETITIONER', 'PLAINTIFF(S)/ PETITIONER', 'PLAINTIFF(S) / PETITIONER', 'PLAINTIFF(S)/PETITIONER',  'Plaintiff', 'Plaintiffs', 'PLAINTIFF', 'Petitioner', 'PETITIONER', 'Debtor', 'Custodial', 'Insured', 'Claimant', 'Judgement Creditor', 'Custodial Party', 'Pltf./Petitioner', 'Plaintiffs Attorney']

    party_title = []
    for defentant in name_list:
        text = defentant
        text = clean(text)

        ratio = []
        temp_list_ratio = []
        temp_list_name = []
        for eachname in plaintiff_keywords:
            eachname_lwr = eachname.lower()
            n = len(eachname.split(" "))

            ngrams = find_Ngrams(text.split(" "),n)

            for i in ngrams:
                if difflib.SequenceMatcher(None,i,eachname_lwr).ratio()*100>95:
                    temp_list_ratio.append(difflib.SequenceMatcher(None,i,eachname_lwr).ratio()*100)
                    temp_list_name.append(eachname)

        if len(temp_list_ratio)>0:
            m = max(temp_list_ratio)
            cc = [i for i, j in enumerate(temp_list_ratio) if j == m]

            tags = []
            for i in cc:
                 tags.append(temp_list_name[i])

            for i in tags:
                if difflib.SequenceMatcher(None,i,"plaintiffs attorney").ratio()*100>95:
                    party_title.append("None")   
                    break
            if len(tags)>0:
                party_title.append(list(set(tags))[0])
            else:
                party_title.append("None")
      
    if len(party_title)>0:
        return list(set(tags))[0]
    else:
        return "None"

        
        
        
def defentant_party_title(name_list):
    defendant_keywords = ['Taxpayer', 'DEFENDANT/RESPONDENT', 'DEFENDANT(s)/RESPONDENT', 'DEFENDANTS/RESPONDENTS', 'DEFENDANT / RESPONDENT', 'DEFENDANT /RESPONDENT', 'Defendant/Respondent', 'Defendant(s)/Respondent', 'Defendants/Respondent', 'Defendants/Respondents', 'Defendant(S)', 'Defendant', 'Defendants', 'DEFENDANT', 'Respondent', 'RESPONDENT', 'Judgement Debtor', 'Obligor', ]
    party_title = []
    temp_list_ratio = []
    temp_list_name = []
    for defentant in name_list:
        text = defentant
        text = clean(text)
        ratio = []
        for eachname in defendant_keywords:
            eachname_lwr = eachname.lower()
            n = len(eachname_lwr.split(" "))

            ngrams = find_Ngrams(text.split(" "),n)

            for i in ngrams:
                if difflib.SequenceMatcher(None,i,eachname_lwr).ratio()*100>75:
                    temp_list_ratio.append(difflib.SequenceMatcher(None,i,eachname_lwr).ratio()*100)
                    temp_list_name.append(eachname)

        if len(temp_list_ratio)>0:
            m = max(temp_list_ratio)
            cc = [i for i, j in enumerate(temp_list_ratio) if j == m]
            tags = []
            for i in cc:
                 tags.append(temp_list_name[i])

            for i in tags:
                if difflib.SequenceMatcher(None,i,"plaintiffs attorney").ratio()*100>95:
                    party_title.append("None")   
                    break
            if len(tags)>0:
                party_title.append(list(set(tags))[0])
            else:
                party_title.append("None")
     
    if len(party_title)>0:
        return list(set(tags))[0]
    else:
        return "None"
