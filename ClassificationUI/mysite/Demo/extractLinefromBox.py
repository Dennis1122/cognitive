import pdfquery
import PyPDF2
import re
from collections import defaultdict,OrderedDict
from operator import itemgetter

def read_line(path,locations):
    """ This function will read text and the cordinates of each of the horizontal boxes within a page of a pdf file"""
    PagePosDict=dict()
    list_keys = list()
    list_values = list()
    pdf=pdfquery.PDFQuery(path)
    i=locations[0][0]
    try:
            pdf.load(i)
            JQuery=pdf.pq('LTPage')
            regex = re.compile('[^a-zA-Z0-9-.?!,"/\';|& ]')
            for j in JQuery("LTTextLineHorizontal"):
                cordinates=list()
                cordinates.append(i)
                cord=JQuery(j).attr('bbox')
                for a in ['[',']']:
                    cord = cord.replace(a,'')
                for a in cord.split(', '):
                    cordinates.append(float(a))
                temp = JQuery(j).text()
                temp = regex.sub('',temp)
                temp = temp.replace("cid9",'')
                if len(temp)>2:
                    PagePosDict[tuple(cordinates)]=temp
            
            for row in range(0,len(locations)):
                xmin = locations[row][1]
                xmax = locations[row][3]
                ymin = locations[row][2]
                ymax = locations[row][4]
                for i in range(0,len(PagePosDict)):
                    if(PagePosDict.keys()[i][1]>=xmin and PagePosDict.keys()[i][3]<=xmax and PagePosDict.keys()[i][2]>=ymin and PagePosDict.keys()[i][4]<=ymax):
                        list_keys.append(PagePosDict.keys()[i])
                row+=1
            keylist = sorted(list_keys, key=itemgetter(2),reverse= True)
            for key in keylist:
                list_values.append(PagePosDict[key])
            i=0
            list_values_new = list()
            while(i<len(list_values)):
                temp_string = list_values[i]
                j = i + 1
                while(j < len(list_values)):
                    count_u = 0
                    count_l = 0
                    for l in list_values[j]:
                        if(l.islower()):
                            count_l+=1
                        elif(l.isupper()):
                            count_u+=1
                    if(len(list_values[j].split())==1 or list_values[j].lower().startswith(('company','inc','corp','llc','ltd')) or list_values[j][0].islower() or (count_l!=0 and float(count_u)/count_l<0.5)):
                        temp_string = temp_string +' '+list_values[j]
                        j += 1
                        i += 1
                    else:
                        break
                list_values_new.append(temp_string)
                i += 1       
    except Exception as e:
        #print e
        return list_values_new
    return list_values_new
        
#line_list = read_line('D:/New folder (2)/530768111_ASB_VA.pdf' ,new_list)