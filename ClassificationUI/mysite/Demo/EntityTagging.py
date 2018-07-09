def entity_tagging(nlp,txt):
    import re
    """This function will do the entity tagging and replace the characters and entities with proper names"""
    txt=txt.decode('utf8')
    doc=nlp(txt)
    txt=""
    for ent in doc:
        if len(ent.ent_type_)==0:
            txt=txt+ent.text+" "
        elif ent.text.upper() in ['DEAR','DOCKET','NO','CIVIL','ACTION','COUNTY','COURT','COMBINED','CLERK','THIRD',                          'JUDICIAL','CIRCUIT','IN','THE','MATTER','OF','THE','ASSESSMENT','WORKERS',                          'COMPENSATION','TAXES','AGAINST','CORPORATION','FILED','DISTRICT','ADDRESS',                                  'CITY','ALL','DEFENSE','COUNSEL','SUPERIOR','STREET','SOCIAL','SECURITY','NUMBER','GARNISHEE','REQUEST','SERVICE'\
                                 'NON', 'EARNINGS', 'GARNISHMENT',\
                                 'FIRST', 'DEFENDANT','PROCESS','SERVER','STATE','ZIP','CASE','ET','AL','CT','BUSINESS'\
                                 'REGISTERED','AGENT','JUDGEMENT','DEBTOR','CREDITOR']:
            txt=txt+ent.text+" "
        elif ent.ent_type_ in ['PERSON','NORP','FACILITY','ORG']:
            txt=txt+"ITSANAME"+" "
        elif ent.ent_type_ in ['ORG']:
            txt=txt+"ITSANORG"+" "
        elif ent.ent_type_ in ['GPE','LOC']:
            txt=txt+"ITSAGPE"+" "
        elif ent.ent_type_ in ['DATE','TIME']:
            txt=txt+"ITSATIME"+" "
        elif ent.ent_type_ in ['PERCENT','MONEY','QUANTITY']:
            txt=txt+"ITSAQUANTITY"+" "
        elif ent.ent_type_ in ['ORDINAL','CARDINAL']:
            txt=txt+"ITSANUMBER"+" "
        else:
            txt=txt+"ITSAENTITY"+" "
            #txt=txt+"ITSANAME"+" "
    txt =txt.replace('cid:9','CID')
    regex = re.compile('[^a-zA-Z0-9 ]')
    data = regex.sub('', txt)
    return data

