def findOrder(order,result):
    pagesNumbers = []
    for eachitem in order:
        for i in range(0,len(result)):
            if result[i]!=0:
                #print eachitem
                if eachitem==result[i][0]:
                    #print result[i][0]
                    pagesNumbers.append(result[i][1])
                    result[i]=0
    
    #print result
    result = list(filter(lambda a: a != 0, result))
    
    for item in result:
        if item[0]!="TRANSMITTAL":
            pagesNumbers.append(item[1])
    
    
    return pagesNumbers


def orderPages(lawsuit,res):
    result = []
    for i in range(0,len(res)):
        result.append((res[i],i))
    if lawsuit=="Subpoena":
        order = ['SUBPOENA','REQUEST','AUTHORIZATION','LETTER']
        
    elif lawsuit=="Asbestos Litigation":
        order = ['COMPLAINT','SUMMONS','NOTICE','ORDER','LETTER','INTERROGATORIES','REQUEST','AFFIDAVIT','JUDGMENT','CERTIFICATE' ]  
        
    elif lawsuit=="Foreclosure Litigation":
        order = ['COMPLAINT','SUMMONS','NOTICE','ORDER','LETTER','INTERROGATORIES','REQUEST','AFFIDAVIT','JUDGMENT','DISMISSAL','CERTIFICATE' ]  
        
    elif lawsuit.find("Garnishm")>=0:
        order = ['WRIT','REQUEST','SUMMONS','COMPLAINT','ORDER','RELEASE','DISMISSAL'] 
        
    elif lawsuit=="Insurance Litigation":
        order = ['COMPLAINT','SUMMONS','NOTICE','ORDER','LETTER','INTERROGATORIES','REQUEST','AFFIDAVIT','JUDGMENT','DISMISSAL','CERTIFICATE' ]   
        
    elif lawsuit=="Levies":
        order = ['NOTICE','DEMAND'] 
        
        
    return findOrder(order,result)
