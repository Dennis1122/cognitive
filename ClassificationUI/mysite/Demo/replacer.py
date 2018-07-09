import re
import myconfig
def replace_county(txt):
    txt_file = open(myconfig.country_list,"r")
    county = []
    for i in txt_file.readlines():
        county.append(i.strip().lower())

    for word in county:

            if txt.find(word)>-1:   

                frm = txt.find(word)
                to = frm+len(word)-1


                if len(word)==len(txt):
                    txt = "ITSAGPE"                    
                if frm==0 and to!=len(word):
                    if txt[to+1].isalpha():
                        pass
                    else:
                        txt = txt.replace(word+txt[to+1],"ITSAGPE"+txt[to+1])
                elif to+1==len(txt):
                    if txt[frm-1].isalpha():
                        pass
                    else:
                        txt = txt.replace(txt[frm-1]+word,txt[frm-1]+"ITSAGPE")
                else:            
                    if txt[to+1].isalpha()==False and txt[frm-1].isalpha()==False:
                        txt = txt.replace(txt[frm-1]+word+txt[to+1],txt[frm-1]+"ITSAGPE"+txt[to+1])


    return txt

def replace_jurisdiction(txt):
    unicode_str = txt.decode('ascii')
    txt = unicode_str.encode('utf-8')
    state_code_dictionary= {'AL':'alabama','MO':'missouri','AK':'alaska','MT':'montana',\
                            'AZ':'arizona','NE':'nebraska','AR':'arkansas','NV':'nevada',\
                            'CA':'california','NH':'new hampshire','CO':'colorado','NJ':'new jersey',\
                            'CT':'connecticut','NM':'new mexico','DE':'delaware','NY':'new york',\
                            'NC':'north carolina','ND':'north dakota','GA':'georgia','OH':'ohio',\
                            'HI':'hawaii','OK':'oklahoma','ID':'idaho','OR':'oregon','IL':'illinois',\
                            'PA':'pennsylvania','indiana':'indiana','RI':'rhode island','IA':'iowa',\
                            'SC':'south carolina','KS':'kansas','SD':'south dakota','KY':'kentucky',\
                            'TN':'tennessee','LA':'louisiana','TX':'texas','ME':'maine','UT':'utah',\
                            'MD':'maryland','VT':'vermont','MA':'massachusetts','VA':'virginia',\
                            'MI':'michigan','WA':'washington','MN':'minnesota','WV':'west virginia',\
                            'FL':'florida','MS':'mississippi','WI':'wisconsin','WY':'wyoming'}
    JS = state_code_dictionary.keys()
    for flag in range(0,2):
        for word in JS:
                
                if txt.find(word)>-1:   

                    if len(word)==len(txt):
                        txt = "ITSAGPE" 

                    frm = txt.find(word)
                    to = frm+len(word)-1

                    if frm==0 and to!=len(word):
                        if txt[to+1].isalpha():
                            pass
                        else:
                            txt = txt.replace(word+txt[to+1],"ITSAGPE"+txt[to+1])
                    elif to+1==len(txt):
                        if txt[frm-1].isalpha():
                            pass
                        else:
                            txt = txt.replace(txt[frm-1]+word,txt[frm-1]+"ITSAGPE")
                    else:            
                        if txt[to+1].isalpha()==False and txt[frm-1].isalpha()==False:
                            txt = txt.replace(txt[frm-1]+word+txt[to+1],txt[frm-1]+"ITSAGPE"+txt[to+1])
        JS = state_code_dictionary.values()
        for eachjs in state_code_dictionary.values():
            JS.append(eachjs.upper()) 

    return  replace_county(txt)
def replace_v(txt):
    """This function will replace v or vs with versus"""
    txt=txt.split(' ')
    data=""
    for word in txt:
        flag=False
        tmp = re.sub('[^a-zA-Z]','',word)
        for v in['vs','v','versus','against']:
            if tmp.lower().find(v)>=0 and len(tmp)<=len(v):
                data=data+"versus"+" "
                flag=True
                break
        if tmp.lower().find('and')>=0 and len(tmp)<=len(v):
            data=data+"and"+" "
            flag=True
        if not flag:
            data+=word
            data+=" "
    data = re.sub(' +',' ',data)
    return data
