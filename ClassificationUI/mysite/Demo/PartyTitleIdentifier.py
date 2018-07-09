import pdfquery
import PyPDF2
import webbrowser
from collections import defaultdict
from pdfreader import read_pdf

def replacePlaintiff(path,pagenum):
    plaintiff_keywords = ['Name(s) and address(es) of Judgment Creditor(s)','Plaintiff\'s name and address (judgment creditor)','Claimant/Applicant','Claimant / Applicant', 'Claimant / Applicant', 'Applicant','PLAINTIFF(S)/PETITIONER', 'PLAINTIFF(S) /PETITIONER', 'PLAINTIFF(S)/ PETITIONER', 'PLAINTIFF(S) / PETITIONER', 'PLAINTIFF(S)/PETITIONER','PLAINTIFF/PETITIONER','Plaintiff/Petitioner', 'Plaintiff(s)', 'Plaintiffs', 'Plaintiff', 'PLAINTIFF', 'Petitioner', 'PETITIONER','Petitioner(s)', 'Employees', 'Employee', 'EMPLOYEE','Employer', 'EMPLOYER', 'Custodial', 'Party', 'Insured', 'Claimant', 'Judgement Creditor', 'Custodial Party', 'Pltf./Petitioner', 'Plaintiffs Attorney','Plaintiff and Garnishor']
    

    plaintiff_keywords= sorted(plaintiff_keywords, key=lambda x: len(x), reverse=True)
    
    #print(defendant_keywords)
    Identifiedpltf=''
    
    Identifiedpage=0
    transvalPlt = ''
    
    #print(page)
    print("\n")
    for val in pagenum:
        for text in plaintiff_keywords:
            page=read_pdf(path,[val])
            if text in page:
                Identifiedpltf=text
                #Identifiedpage=val
                
                if text=='Plaintiffs' or text=='Plaintiff/Petitioner':
                    transvalPlt = 'Pltfs.'
                    break
                elif text=='Plaintiff' or text=='PLAINTIFF' or text=='PLAINTIFF(S)' or text=='Plaintiff(s)' or text=='Plaintiffs Attorney' or text=='Plaintiff and Garnishor' or text=='Party' or text=='Employee' or text=='Employer' or text=='Employees' or text=='EMPLOYEE' or text=='EMPLOYER':
                    transvalPlt = 'Pltf.'
                    break
                elif text=='Plaintiff\'s name and address (judgment creditor)' or text=='Plaintiff/Judgment Creditor':
                    transvalPlt = 'Pltf./Judgement Creditor'
                    break
                elif text=='Name(s) and address(es) of Judgment Creditor(s)':
                    transvalPlt = 'Pltf.'
                    break
                elif text=='Claimant / Applicant':
                    transvalPlt = 'Claimant/Applicant'
                    break
    #------------------CHECK CASE BELOW---------------   
                elif text=='PLAINTIFF/PETITIONER':
                    transvalPlt = 'Pltf./Petitioner'
                    break
    #-------------------------------------------------
                elif text=='Petitioner(s)':
                    transvalPlt = 'Petitioner'
                    break
                elif text not in plaintiff_keywords:
                    transvalPlt='Pltf.'
                    break
                else:
                    transvalPlt=text
                    break
                break
   
    if transvalPlt=='':
        transvalPlt='Pltf'
    return transvalPlt


# In[180]:

def replaceDefendant(path,pagenum):
    defendant_keywords = ['Name(s) and address(es) of Judgment Debtor(s)','Defendant\'s name and address (judgment debtor)','Garnishee','GARNISHEE DEFENDANT','Employer / Insurance Carrier / Defendant','Employer/Insurance Carrier/Defendant','DEFENDANT/RESPONDENT', 'DEFENDANT(s)/RESPONDENT', 'DEFENDANTS/RESPONDENTS', 'DEFENDANT / RESPONDENT', 'DEFENDANT /RESPONDENT', 'Defendant/Respondent', 'Defendant(s)/Respondent', 'Defendants/Respondent', 'Defendants/Respondents', 'Defendant(S)','Defendant(s)', 'Defendants', 'Defendant', 'DEFENDANT', 'Respondent(s)', 'Respondent', 'RESPONDENT', 'Debtor', 'Employers', 'Employer', 'EMPLOYER', 'Employee', 'EMPLOYEE', 'Judgement Debtor', 'Obligor', 'Taxpayer']
    defendant_keywords= sorted(defendant_keywords, key=lambda x: len(x), reverse=True)
    Identifieddefd=''
    transvalDft = ''
    
                 
    for val in pagenum:
        for text in defendant_keywords:
            page=read_pdf(path,[val])
            if text in page:
                #print(val,text)
                Identifieddefd=text
                
                #Identifiedpage=val 


                if text=='Employer/Insurance Carrier/Defendant':
                    transvalDft='Employer/Insurance Carrier/Dft'
                    break
                elif text=='Defendants' or text=='Defendant/Respondent' or text=='Defendant(s)':
                    transvalDft = 'Dfts.'
                    break
                elif text=='Defendant(S)' or text=='Defendant' or text=='DEFENDANT' or text=='GARNISHEE DEFENDANT' or text=='Garnishee':
                    transvalDft = 'Dft.'
                    break
                elif text=='Defendant\'s name and address (judgment debtor)' or text=='Defendant/Judgment Debtor':
                    transvalDft = 'Dft./Judgment Debtor'
                    break
                elif text=='Name(s) and address(es) of Judgment Debtor(s)':
                    transvalDft = 'Dft.'
                    break
                elif text=='Name(s) and address(es) of Judgment Debtor(s)':
                    transvalDft = 'Dft.'
                    break
                elif text=='Employer / Insurance Carrier / Defendant':
                    transvalDft = 'Employer/Insurance Carrier/Dft.'
                    break
    #------------------CHECK CASE BELOW---------------
                elif text=='DEFENDANT/RESPONDENT' or text=='Defendant(s)/Respondent':
                    transvalDft = 'Dft./Respondents'
                    break
                elif text=='EMPLOYEE':
                    transvalDft = 'Employee'
                    break
                elif text=='EMPLOYER':
                    transvalDft = 'Employer'
                    break
    #-------------------------------------------------
                elif text=='Respondent(s)':
                    transvalDft = 'Respondent'
                    break
                elif text not in defendant_keywords:
                    transvalDft='Dft.'
                    break
                else:
                    transvalDft=text
                    break
                
                break
    if transvalDft=='':
        transvalDft='Dft'
    return  transvalDft
