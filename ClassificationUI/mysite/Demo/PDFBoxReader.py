
# coding: utf-8

# In[7]:

def read_cordinates(path,page_no=None):
    """This function will read contents from the pages mentioned"""
    import pdfquery
    from collections import defaultdict
    """ This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file"""
    PagePosDict=defaultdict()
    pdf=pdfquery.PDFQuery(path)
    if page_no==None:
        page_no=range(6)
    global PLAINTIFF,DEFENDANT
    try:
            for i in page_no:
                    pdf.load(i)
                    JQuery=pdf.pq('LTPage')
                    if JQuery.text().find('Service of Process Transmittal')>=0 :
                        #i+=1 
                        continue
                    for j in JQuery("LTTextBoxHorizontal"):
                        cordinates=list()
                        cordinates.append(i)
                        cord=JQuery(j).attr('bbox')
                        for a in ['[',']']:
                            cord = cord.replace(a,'')
                        for a in cord.split(', '):
                            cordinates.append(float(a))
                        PagePosDict[tuple(cordinates)]=JQuery(j).text()
                    #i+=1
    except Exception:
        return (PagePosDict)
    return (PagePosDict)

