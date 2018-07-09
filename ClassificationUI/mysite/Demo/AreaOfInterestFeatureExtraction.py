def search_text_near_locations(PagePosDict,locations,xbias=50,ybias=50):
    import re
    nearby_locations=[]
    top=[]
    below=[]
    for loc in locations:
        #print "location:", loc
        x_min=loc[1]-xbias
        #print "x min",x_min
        x_max=loc[3]+xbias
        #print "x max",x_max
        y_min=loc[2]-ybias
        #print "y min",y_min
        y_max=loc[4]+ybias
        #print "y max",y_max
        for key in PagePosDict.keys():
            if key[0]==loc[0] and key != loc :
                x=(key[1]+key[3])/2
                #print "xcenter",x
                y=(key[2]+key[4])/2
                #print "ycenter",y
                if x >= x_min and x <= x_max and y>= y_min and y<=y_max:
                    txt=PagePosDict[key]
                    txt=u''.join(txt).encode('utf-8').strip()
                    regex = re.compile('[^a-zA-Z0-9 ]')
                    data = regex.sub(' ', txt)
                    data = data.replace("\xc2\xa0"," ")
                    data=data.replace("cid 9","")
                    data = data.replace("\n\n\n"," ")
                    data = re.sub(' +',' ',data)
                    data = re.sub("[0-9]+","<num>",data)
                    
                    if y <=loc[2] and not(data.find('<num>')>=0 and len(data.strip())<=10):
                        below.append(key)
                    elif y >= loc[4] and not(data.find('<num>')>=0 and len(data.strip())<=10):
                        top.append(key)
                    #nearby_locations.append(key)
                    """if y <=loc[2]:
                        below.append(key)
                    elif y >= loc[4]:
                        top.append(key)"""
        if len(below) > 1:
            #print "below : ", below
            nearby_locations.append(find_first_below(below))
        elif len(below)==1:
            #print "below : 1"
            nearby_locations.append(below[0])
        if len(top) > 1:    
            #print "Top :", top
            nearby_locations.append(find_first_top(top))
        elif len(top)==1:
            #print "top : 1"
            nearby_locations.append(top[0])                    
        
    return nearby_locations
def identify_nearby_text(text_loc,nearby_locs,PagePosDict):
    nearby_txt_y_top=[]
    nearby_txt_y_below=[]
    text_loc=text_loc[0]
    if nearby_locs and text_loc:
        for loc in nearby_locs:
            if loc == text_loc:
                    continue
            if (loc[2]+loc[4])/2 <= text_loc[2]:
                nearby_txt_y_below.append(PagePosDict[loc])
            elif (loc[2]+loc[4])/2 >= text_loc[4]:
                nearby_txt_y_top.append(PagePosDict[loc])
        return (nearby_txt_y_top,nearby_txt_y_below)
    else:
        return 0
def find_first_top(cordinates):
    y=[]
    for cords in cordinates:
        y.append(cords[2])
    for cords in cordinates:
        if cords[2]==min(y):
            #print "Length of cordinates", len(cords)
            return cords

            
def find_first_below(cordinates):
    y=[]
    for cords in cordinates:
        y.append(cords[2])
    for cords in cordinates:
        if cords[2]==max(y):
            #print "Length of cordinates", len(cords)
            return cords

