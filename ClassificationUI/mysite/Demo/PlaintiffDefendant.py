from Levies_plaintiff import plaintiff_levies

import pdfquery
import datetime
import re
from collections import defaultdict
from sklearn.externals import joblib
from Dftd_Filter import filter_prediction as DFTD
from Pltf_Filter import filter_prediction as PLTF
from replacer import replace_jurisdiction as replace_county
from replacer import replace_v
from FinalExtraction import extractor_plaintiff,extractor_defendant
from EntityTagging import entity_tagging
import spacy
nlp = spacy.load('en')
import difflib
from AreaOfInterestFeatureExtraction import search_text_near_locations,identify_nearby_text
from POSTagging import find_pos_tags
from AttachmentsOrdering import orderPages
from extractLinefromBox import read_line
import myconfig
import json
from loger import logger
import Error_Handler
clf=joblib.load(myconfig.pldf_RFv4)
text_vectorizer_pltf=joblib.load(myconfig.pldf_text_vectorizer)
top_vectorizer_pltf=joblib.load(myconfig.pldf_top_vectorizer)
below_vectorizer_pltf=joblib.load(myconfig.pldf_below_vectorizer)
text_vectorizer_dftd=joblib.load(myconfig.dftd_text_vectorizer)
top_vectorizer_dftd=joblib.load(myconfig.dftd_top_vectorizer)
below_vectorizer_dftd=joblib.load(myconfig.dftd_below_vectorizer)
text_vectorizer_zero=joblib.load(myconfig.pldfdftd_text_vectorizer)
top_vectorizer_zero=joblib.load(myconfig.pldfdftd_top_vectorizer)
below_vectorizer_zero=joblib.load(myconfig.pldfdftd_below_vectorizer)


class PltfDftd:
    def read_cordinates(self,PagePosDict):

        """ This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file"""

        
        X_tags = []
        X_txt = []
        X_top = []
        X_below = []
        X_cordinate = []
        original_txt = []
        original_top = []
        original_below = []
        doc_contents = []
        CleanPagePosDict = defaultdict()
        doc_keys = []
        #    #print "For loop on PagePosDict Begins",('{:%H:%M:%S}'.format(datetime.datetime.now()))

        for key in sorted(PagePosDict):
            try:
                txt = PagePosDict[key]
                txt = u''.join(txt).encode('utf-8').strip()
                regex = re.compile('[^a-zA-Z0-9-.?!,":\';()|\& ]')
                data = regex.sub('', txt)
                data = data.replace("\xc2\xa0", " ")
                data = data.replace("\n\n\n", "\n")
                data = re.sub(' +', ' ', data)
                data = data.replace('&', 'and')
                doc_contents.append(data)
                doc_keys.append(key)
                PagePosDict[key] = data
            except Exception as e:
                # print "Exception at sorting", e
                continue
                #    #print "For loop on PagePosDict Ends",('{:%H:%M:%S}'.format(datetime.datetime.now()))
        counts = 0

        #    #print "For loop on doc_keys,doc_contents begins", ('{:%H:%M:%S}'.format(datetime.datetime.now()))
        for cordinate, txt in zip(doc_keys, doc_contents):
            nearby_txt_top = ""
            nearby_txt_below = ""
            content = ""
            locations = []
            nearby_locs = search_text_near_locations(PagePosDict, [cordinate])
            nearby_txt = identify_nearby_text([cordinate], nearby_locs, PagePosDict)
            # print "Text","\n",txt
            if nearby_txt != 0:
                nearby_txt_top = u' '.join(content for content in nearby_txt[0])
                nearby_txt_below = u' '.join(content for content in nearby_txt[1])
            else:
                continue
            original_txt.append(txt)
            txt = self.clean_txt(txt)
            X_txt.append(txt)
            top = nearby_txt_top
            below = nearby_txt_below
            original_top.append(top)
            original_below.append(below)
            X_cordinate.append(cordinate)
            X_tags.append(find_pos_tags(txt))
            nearby_txt_top = self.clean_txt(top)
            nearby_txt_below = self.clean_txt(below)
            X_top.append(nearby_txt_top)
            X_below.append(nearby_txt_below)
        # print original_txt,original_top,original_below,X_txt,X_top,X_below,X_cordinate,X_tag
        return (original_txt, original_top, original_below, X_txt, X_top, X_below, X_cordinate, X_tags)

    def __init__(self, esop_id, path,PageDict):
        self.esop_id = esop_id
        self.path = path
        self.PageDict=PageDict
    def clean_txt(self,data):
        data=replace_county(replace_v(entity_tagging(nlp,data)))
        data = re.sub(' +',' ',data)
        data=re.sub('[0-9]+','digit',data)
        regex = re.compile('[^a-zA-Z]')
        tmp = regex.sub('', data)
        if len(tmp)<3:
            return "BLANKLINE"
        else:
            return data
    def predict(self,law,attach):
      try:
        logger.info("started from pltfdftd "+ str(self.esop_id))
        #path="/home/1232301/PycharmProjects/WK-FINAL-without-kafka/testdocs/531104590_FC_UT.pdf"
        litigation=law
        attachments=attach
        pageOrder=orderPages(litigation,attachments)
        final_plaintiff=None
        final_defendant=None
        involuntary_plaintiff=[]
        pltfdftdVS = []
        pltfdftdPartyTitle = []
        cs_score =[]
        cs_pltf = 0
        cs_dftd = 0
        for page in pageOrder:
            if final_plaintiff != None and final_defendant != None:
                break
            X = []
            party_title_details = []
            pltf_aftr_filtering = []
            dftd_aftr_filtering = []
            plaintiff = []
            defendant = []
            pltf_index_level1 = []
            dftd_index_level1 = []
            original_txt, original_top, original_below, X_txt, X_top, X_below, X_cordinate, X_tags = self.read_cordinates(
                self.PageDict[page])
            for xp1, xp2, xp3, x4, xd1, xd2, xd3, xz1, xz2, xz3 in \
                    zip(text_vectorizer_pltf.transform(X_txt).toarray(), \
                        top_vectorizer_pltf.transform(X_top).toarray(), \
                        below_vectorizer_pltf.transform(X_below).toarray(), X_tags, \
                        text_vectorizer_dftd.transform(X_txt).toarray(), \
                        top_vectorizer_dftd.transform(X_top).toarray(),
                        below_vectorizer_dftd.transform(X_below).toarray(), \
                        text_vectorizer_zero.transform(X_txt).toarray(), \
                        top_vectorizer_zero.transform(X_top).toarray(),
                        below_vectorizer_zero.transform(X_below).toarray(), ):
                tmp = []
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
            if len(X) > 0:
                result_level1 = clf.predict(X)
                cs_score=clf.predict_proba(X)
            else:
                continue
            pltf_index_level1 = [a for a in range(len(result_level1)) if result_level1[a] == 1]
            dftd_index_level1 = [a for a in range(len(result_level1)) if result_level1[a] == 2]
            if final_plaintiff == None and len(pltf_index_level1) > 0:
                for index in pltf_index_level1:
                    txt = X_txt[index]
                    top = X_top[index]
                    below = X_below[index]
                    pltf = original_txt[index]
                    plaintiff.append(pltf)
                    out = pltf + "#" + top + "#" + below + "#" + "\n"
                    party_title_details.append(out)
                    if PLTF(txt, top, below) == 1:
                        pltf_aftr_filtering.append(pltf)
                        # print pltf_aftr_filtering
                        temp = replace_v(pltf)
                        if temp.find('versus') > 5:
                            pltfdftdVS.append(pltf)
                            pltfdftdPartyTitle.append(out)
                if len(pltf_aftr_filtering) > 0:
                    final_plaintiff = extractor_plaintiff(pltf_aftr_filtering, party_title_details,
                                                          involuntary_plaintiff)
                    cs_pltf=max(cs_score[index])
            logger.info("before final_defendant == None"+ str(self.esop_id))
            if final_defendant == None and len(dftd_index_level1) > 0:
                totalArea = []
                for index in dftd_index_level1:
                    txt = X_txt[index]
                    top = X_top[index]
                    below = X_below[index]
                    tags = X_tags[index]
                    dftd = original_txt[index]
                    defendant.append(dftd)
                    if DFTD(txt, top, below, tags) == 1:
                        dftd_aftr_filtering.append(defendant)
                        out = dftd + '#' + top + '#' + below + '#'
                        party_title_details.append(out)
                        temp = replace_v(dftd)
                        if temp.find('versus') > 5:
                            pltfdftdVS.append(dftd)
                            pltfdftdPartyTitle.append(out)
                        totalArea.append(X_cordinate[index])
                c = 0
                logger.info("before final_defendant == None"+ str(self.esop_id))
                if len(totalArea) != 0:
                    dftd_aftr_filtering = []
                    for dft in read_line(self.path, totalArea):
                        c += 1
                        for phrases in ['AFFIDAVIT FOR GARNISHMENT', 'AGAINST BANK ACCOUNT']:
                            if difflib.SequenceMatcher(None, dft, phrases).ratio() * 100 >= 90:
                                continue
                        if len(dft.strip()) <= 3:
                            continue
                        dftd_aftr_filtering.append(dft.replace('(cid:9)', ''))
                if len(dftd_aftr_filtering) > 0:
                    final_defendant = extractor_defendant(dftd_aftr_filtering,
                                                          party_title_details).strip() + '  //  To:'
                    cs_dftd=max(cs_score[index])
                    # print "Final Defendant 1"
                    # print "Plaintiff after processing page ",page,"is",final_plaintiff
                    # print "Defendant after processing page ",page,"is",final_defendant
        if final_plaintiff == None and litigation.lower().find('lev') >= 0:
            final_plaintiff,cs_pltf = plaintiff_levies(self.path)
            cs_pltf = 0.86
            # print "Plaintiff identified at 2"
        elif final_plaintiff == None and len(pltfdftdVS) > 0:
            final_plaintiff = extractor_plaintiff(pltfdftdVS, pltfdftdPartyTitle, involuntary_plaintiff)
            cs_pltf = 0.76
            # print "Plaintiff identified at 3"
        elif final_plaintiff == None and len(pltf_index_level1) != 0:
            final_plaintiff = extractor_plaintiff([original_txt[pltf_index_level1[0]]], [''], involuntary_plaintiff)
            cs_pltf = 0.64
            # print "Plaintiff identified at 4"
        if final_defendant == None and len(pltfdftdVS) != 0:
            final_defendant = extractor_defendant(pltfdftdVS, pltfdftdPartyTitle)
            cs_dftd = 0.84
            # print "Final Defendant 2"
        elif final_defendant == None and len(dftd_index_level1) != 0:
            totalArea = [X_cordinate[dftd_index_level1[0]]]
            if len(totalArea) != 0:
                dftd_aftr_filtering = []
                for dft in read_line(self.path, totalArea):
                    c += 1
                    for phrases in ['AFFIDAVIT FOR GARNISHMENT', 'AGAINST BANK ACCOUNT']:
                        if difflib.SequenceMatcher(None, dft, phrases).ratio() * 100 >= 90:
                            continue
                    if len(dft.strip()) <= 3:
                        continue
                    dftd_aftr_filtering.append(dft.replace('(cid:9)', ''))
                if len(dftd_aftr_filtering) > 0:
                    final_defendant = extractor_defendant(dftd_aftr_filtering, [''])
                    # print "Final Defendant 3"
        #print "Story Ends :", ('{:%H:%M:%S}'.format(datetime.datetime.now()))
        if final_plaintiff == None:
            final_plaintiff = 'None'
        if final_defendant == None:
            final_defendant = 'None'
		
        result = {"esop_id": self.esop_id, "pltf": final_plaintiff, "pltf_cs": cs_pltf,"dftd": final_defendant, "dftd_cs": cs_dftd}
        result_final = json.dumps(result)
        logger.info("sent result from pltfdftd "+ str(self.esop_id))
        return result_final
      except Exception,e:
        logger.info("exception from pltfdftd " +str(e)+ str(self.esop_id))
        error_handler = Error_Handler.Error_Handler()
        error_handler.mysql_insert_error("pltfdftd",myconfig.error_code2,str(self.esop_id)+" "+str(e))