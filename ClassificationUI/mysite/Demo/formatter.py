import re
def final_format(txt):
    txt = txt.strip()
    txt = re.sub(' +',' ',txt)
    """for i in range(len(txt)):
        if txt[i].isalpha():
            txt = txt[i:]
            break
        else:
            i=i+1"""
    txt = txt.replace("premiere predit of north america, llc and premiere credit, insureds.","Premiere Credit Of North America, LLC,")
    words=txt.split(' ')
    cleanedTxt=""
    for i in range(0,len(words)):
        j=0
        while not words[i][j].isalpha():
            j=j+1
            if j==len(words[i]):
                break
        word = words[i][0:j+1].upper()+words[i][j+1:len(words[i])].lower()
        cleanedTxt+=word+' '

    corp_indicators = ['LLC', 'LP', 'LLP']
    words=cleanedTxt.split(' ')
    
    for eachindicator in corp_indicators:
        for i in range(0,len(words)):
            if words[i].lower().find(eachindicator.lower())>=0:
                start = words[i].lower().find(eachindicator.lower())
                end = start + len(eachindicator)
                to_replace = words[i][start:end]
                words[i] = words[i].replace(to_replace,eachindicator)

    cleanedTxt = ' '.join(words)
    
    cleanedTxt = re.sub(' +',' ',cleanedTxt)
    cleanedTxt = re.sub('\.+','.',cleanedTxt)
    cleanedTxt = re.sub(',+',',',cleanedTxt)
    cleanedTxt = cleanedTxt.replace(' ,',',')
    cleanedTxt = cleanedTxt.replace("Et Al","et al")
    cleanedTxt = cleanedTxt.replace("Etc","etc")
    cleanedTxt = cleanedTxt.replace("L.l.c.","L.L.C.")
    cleanedTxt = cleanedTxt.replace("et al., etc.,","etc., et al.,")
    cleanedTxt = re.sub(',+',',',cleanedTxt)
    for i in range(0,len(cleanedTxt)):
        if str(cleanedTxt[i]).isalnum():
            break
    cleanedTxt = cleanedTxt[i:len(cleanedTxt)]
    cleanedTxt = cleanedTxt.replace(";","")
    cleanedTxt = cleanedTxt.strip()
    cleanedTxt = re.sub(r'\b(.+)\s+\1\b', r'\1', cleanedTxt)
    if cleanedTxt[-3:]=="Dft" or cleanedTxt[-4:]=="Dfts" or cleanedTxt[-4:]=="Pltf" or cleanedTxt[-5:]=="Pltfs":
        return cleanedTxt+"."
    else:
        return cleanedTxt 



def format_name(names,descriptions,party_title):
    
    #print (names,descriptions,party_title)
    
    if len(names)==0:
        return 'None'
    
    party_title=party_title[0].upper()+party_title[1:].lower()
    defendant = ""
    temp_names = []
    temp_descriptions = []
    
    for name,description in zip(names,descriptions):
        name = name.replace("et al ","et al.")
        name = name.replace("et al","et al.")
        name = name.replace("ET AL ","et al.")
        name = name.replace("ET AL.","et al.")
        name = name.replace(" ET AL"," et al.")
        name = name.replace("et. al.","et al.")
        name = name.replace("et al.,","et al.")
        name = name.replace("ET Al.","et al.")
        name = name.replace(" etal."," et al.")
        name = name.replace(" et al.,"," et al.")
        name = name.replace(" etaL"," et al.")
        if name.find(" et al.")>=0:
            name = name[0:name.find(" et al.")+len(" et al.")]
            name = name.replace(" et al."," et al.,")
        temp_names.append(name.strip())
        
        desc = description.replace("etc","etc.,")
        temp_descriptions.append(desc.strip(" "))
        
    if len(temp_names)==1:

        defendant =  temp_names[0]+", "+temp_descriptions[0]+" "+party_title
        defendant = re.sub(' +',' ',defendant)
        defendant = re.sub(',+',',',defendant)
        defendant = re.sub('\.+','.',defendant)
        name_unformated = temp_names[0]
        des = temp_descriptions[0]

        if name_unformated.find("et al")>=0:
            if name[name.find(" et al")-1]==",":
                defendant =  name+" "+party_title+"s"
            else:
                name = name.replace(" et al",", et al")
                defendant =  name+", "+party_title+"s"
                
            if des.find("etc")>=0:
                defendant = name+", etc., "+party_title+"s"
                if desc.find("etc")>=0:
                    s = name
                    d =', etc., '
                    defendant = s+d+party_title+"s"
            return final_format(defendant)
        return final_format(defendant)

    if len(temp_names)==2:
        
        name = ' '.join(temp_names)
        desc = ' '.join(temp_descriptions)
        if name.find("et al")<0 and desc.find('etc')<0:
            defendant =  temp_names[0]+" and "+temp_names[1]+", "+party_title+"s"
            defendant = re.sub(' +',' ',defendant)
            defendant = re.sub(',+',',',defendant)
            defendant = re.sub('\.+','.',defendant)

            return final_format(defendant)
    

    if len(temp_names)==2:
        name = temp_names[0]
        des = temp_descriptions[0]
        if name.find("et al")>=0:   
            if name[name.find(" et al")-1]==",":
                defendant =  name+"., "+party_title+"s"
            else:
                name = name.replace(" et al",", et al")
                defendant =  name+", "+party_title+"s"

            if des.find("etc")>=0:
                defendant = name+", etc., "+party_title+"s"               
                
            if des.find("etc")>=0:
                s = defendant
                d ='etc., '
                s = s[:s.find('et al')]
                defendant = s+d+' et al., '+party_title+"s"
                
            defendant = re.sub(' +',' ',defendant)
            defendant = re.sub(',+',',',defendant)
            defendant = re.sub('\.+','.',defendant) 
            return final_format(defendant)

        if temp_descriptions[0].strip().find("etc")>=0:
            defendant =  temp_names[0]+", etc., and "+temp_names[1]+" "+party_title+"s"
        if temp_descriptions[1].strip().find("etc")>=0:
            defendant =  temp_names[0]+" and "+temp_names[1]+", etc., "+party_title+"s"
        if temp_descriptions[0].strip().find("etc")>=0 and temp_descriptions[1].strip().find("etc")>=0:
            defendant =  temp_names[0]+", etc., and "+temp_names[1]+", etc., "+party_title+"s"   
        if temp_descriptions[0].strip().find("etc")<0 and temp_descriptions[1].strip().find("etc")<0:
            defendant =  temp_names[0]+" and "+temp_names[1]+" "+party_title+"s" 

        defendant = re.sub(' +',' ',defendant)
        defendant = re.sub(',+',',',defendant)
        defendant = re.sub('\.+','.',defendant)
        return final_format(defendant)
        
    if len(temp_names)>2:
        name = temp_names[0]
        desc = temp_descriptions[0]
        if desc.find("etc")>=0:
            s = name
            d =', etc., '
            defendant = s+d+' et al., '+party_title+"s"
            defendant = re.sub(' +',' ',defendant)
            defendant = re.sub(',+',',',defendant)
            defendant = re.sub('\.+','.',defendant)
            return final_format(defendant) 
        
        defendant =  temp_names[0]+", et al., "+party_title+"s"
        defendant = re.sub(' +',' ',defendant)
        defendant = re.sub(',+',',',defendant)
        defendant = re.sub('\.+','.',defendant)
        return final_format(defendant)
    
    defendant =  temp_names[0]+", "+party_title
    defendant = re.sub(' +',' ',defendant)
    defendant = re.sub(',+',',',defendant)
    defendant = re.sub('\.+','.',defendant)
    return final_format(defendant)
