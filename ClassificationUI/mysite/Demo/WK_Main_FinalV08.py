import Attachment
import Lawsuit
import Jurisdiction
import json
import casenumber_v1 as casenumber
import PlaintiffDefendant
from loger import logger
import myconfig
from os import listdir
from os.path import isfile, join
import multiprocessing
import time
import os
import Error_Handler
import pdfquery
from collections import defaultdict
import unicodedata
from collections import defaultdict
from StringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import pdfquery
import PyPDF2
def PDFReader(path,pages=None):
        PagePosDict=[]
        PagePosDict1=[]
        PagePosDictCord=defaultdict()
        PagePosDictPages=defaultdict()
        PagePosDictJuris=[]
        all_pages = []
        all_pages_juris=[]
        all_page_set=[]      
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        manager = PDFResourceManager()
        fd = open(path, 'rb')
        page_no=0
        for page in PDFPage.get_pages(fd, pagenums):
            output = StringIO()
            converter = TextConverter(manager, output, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, converter)
            interpreter.process_page(page)
            doc = output.getvalue()
            all_pages.append(doc)
            if doc[:18] == "Service of Process":
                    continue
            else:
                page_no = page_no + 1
                if page_no <= 5:
                    all_pages_juris.append(doc) 
            converter.close()
            output.close()
        all_page_set.append(' '.join(all_pages_juris))
        fd.close()
        
        i=0        
        pdf=pdfquery.PDFQuery(path)
        try:
            while i<=30:
                pdf.load(i)
                JQuery=pdf.pq('LTPage')
                
                if JQuery.text().find('Service of Process Transmittal')>=0:
                    i+=1
                    continue
                j=0
                LineLength = len(JQuery("LTTextLineHorizontal"))
                BoxLength  = len(JQuery("LTTextBoxHorizontal"))
                if LineLength==0:
                    return 1,PagePosDict,PagePosDict1,PagePosDictCord,all_pages,all_page_set,PagePosDictJuris,PagePosDictPages
                
                if LineLength<BoxLength:
                    NetLength=BoxLength
                else: 
                    NetLength=LineLength            
                PagePosDictPage=defaultdict()
                while (j<NetLength) :
                    
                    if j<LineLength and i<=30 :
                        PagePosDict.append(JQuery(JQuery("LTTextLineHorizontal")[j]).text())
                        cordinates = list()
                        cordinates.append(i)                        
                        cord = JQuery(JQuery("LTTextLineHorizontal")[j]).attr('bbox')
                        for a in ['[', ']']:
                            cord = cord.replace(a, '')                        
                        for a in cord.split(', '):
                            cordinates.append(float(a))                    
                        PagePosDictCord[tuple(cordinates)] = JQuery(JQuery("LTTextLineHorizontal")[j]).text()
                    if j<BoxLength and i<=30 :
                        PagePosDict1.append(JQuery(JQuery("LTTextBoxHorizontal")[j]).text())
                        cordinates = list()
                        cordinates.append(i)                        
                        cord = JQuery(JQuery("LTTextBoxHorizontal")[j]).attr('bbox')
                        for a in ['[', ']']:
                            cord = cord.replace(a, '')                        
                        for a in cord.split(', '):
                            cordinates.append(float(a))                    
                        PagePosDictPage[tuple(cordinates)] = JQuery(JQuery("LTTextBoxHorizontal")[j]).text()                      
                    if j<BoxLength and i<=7 :
                        PagePosDictJuris.append(JQuery(JQuery("LTTextBoxHorizontal")[j]).text())
                    j+=1                  
                PagePosDictPages[i]=PagePosDictPage
                i+=1
                
        except Exception,e: 
            return 0,PagePosDict,PagePosDict1,PagePosDictCord,all_pages,all_page_set,PagePosDictJuris,PagePosDictPages
        return 0,PagePosDict,PagePosDict1,PagePosDictCord,all_pages,all_page_set,PagePosDictJuris,PagePosDictPages

  
def mysql_insert(jsonData):
	con = mdb.connect(myconfig.mysql_server, myconfig.mysql_username,
						   myconfig.mysql_pass, myconfig.mysql_db)
	cursor = con.cursor()
	add_value = ("INSERT INTO Vsop_extract_ml_TCS "
				 "(ESOP_ID,VENDOR_ID,JURISDICTION,JURISDICTION_CS,DOCUMENT_TYPE,"
				 "DOCUMENT_TYPE_CS,LAWSUIT_TYPE,LAWSUIT_TYPE_CS,CASE_NUMBER,CASE_NUMBER_CS,CREATED_DATE,DEFENDANT,DEFENDANT_CS,PLAINTIFF,PLAINTIFF_CS) "
				 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
	data_value = (int(jsonData['esop_id']), int(myconfig.vendor_id), jsonData['jurisdiction'] if 'jurisdiction' in jsonData else "Null",
				  round(jsonData['jurisdiction_cs'],2) if 'jurisdiction_cs' in jsonData else None,jsonData['attachment'] if 'attachment' in jsonData else "Null" ,
				  round(jsonData['attachment_cs'],2) if 'attachment_cs' in jsonData else None, jsonData['lawsuit'] if 'lawsuit' in jsonData else "Null",
				  round(jsonData['lawsuit_cs'],2) if 'lawsuit_cs' in jsonData else None,jsonData['casenumber'] if 'casenumber' in jsonData else "Null",
          round(jsonData['casenumber_cs'],2) if 'casenumber_cs' in jsonData else None,time.strftime('%Y-%m-%d %H:%M:%S'),jsonData['dftd'] if 'dftd' in jsonData else "Null",round(jsonData['dftd_cs'],2) if 'dftd_cs' in jsonData else None,jsonData['pltf'] if 'pltf' in jsonData else "Null",
          round(jsonData['pltf_cs'],2) if 'pltf_cs' in jsonData else None)
	try:
		cursor.execute(add_value, data_value)
		print "success"
	except Exception, e:
		logger.error("An error has occurred"+str(e))
		con.rollback()
	else:
		con.commit()
		
	cursor.close()
	con.close()
		
def mySQL_query():
  data = []
  con = mdb.connect(myconfig.mysql_server, myconfig.mysql_username,myconfig.mysql_pass, myconfig.mysql_db);
  cursor = con.cursor()
  esop_id = 0
  try:
    cursor.execute('SELECT MAX(ESOP_ID) FROM Vsop_extract_ml_TCS')
    esop_id = cursor.fetchone()[0]
    if esop_id == None:
      esop_id = 0
  except Exception, e:
    print "An error has occurred"+str(e)
    esop_id = 0
  try:
    query_select = "SELECT A.ESOP_ID,A.DOC_URL FROM Vesop_inbox_ml A WHERE NOT EXISTS (SELECT B.ESOP_ID FROM Vsop_extract_ml_TCS B WHERE A.ESOP_ID = B.ESOP_ID) AND DOC_URL IS NOT NULL LIMIT %s"
    cursor.execute(query_select,(myconfig.pdf_count,))
    data = cursor.fetchall()
  except Exception, e:
    print "An error has occurred"+str(e)
  cursor.close()
  con.close()
  return data

def s3PdfAccess(url,target_path):
  try:
    url = url.strip()
    s3_client = boto3.client('s3')
    bucket, key = url.split('/',0)[-1].split('/',1)
    fname = key.rsplit('/',1)[1]
    s3_client.download_file(bucket, key, target_path + '/' + fname)
    return fname	
  except Exception,e:
      logger.info("-Not able to download file from s3-"+str(e)+str(url))
      error_handler = Error_Handler.Error_Handler()
      error_handler.mysql_insert_error("S3_download",myconfig.error_code3,str(url)+" "+str(e))

def pdf_process(path,esop_id=1):
    final_result={}
    try:
      logger.info("Downloading PDF for esop"+str(esop_id)+"for PDF")
      pdf_read=PDFReader(path)
      if(pdf_read[0]==0):
        if(path.endswith(".pdf")):
          logger.info("starting OCR PDF extraction for esop--"+str(esop_id))
          attachment = Attachment.Attachment(esop_id, pdf_read[4])
          jurisdiction = Jurisdiction.Jurisdiction(esop_id, pdf_read[6],pdf_read[5])
          lawsuit = Lawsuit.Lawsuit(esop_id, pdf_read[4])
          caseno = casenumber.CaseNumber(esop_id, pdf_read[1],pdf_read[2],pdf_read[3])
          pool = multiprocessing.Pool(4)
          results = pool.map(run_mdules_pool, [attachment, jurisdiction, lawsuit, caseno])
          for result in results:
            final_result.update(result)
          pool.close()
          pool.join()
          attach = final_result['attachment'].split("#")
          attachment_pltf = []
          for i in attach:
            attachment_pltf.append(unicodedata.normalize('NFKD', i).encode('ascii','ignore'))
          law = final_result['lawsuit']
          pltfdftd = PlaintiffDefendant.PltfDftd(esop_id, path,pdf_read[7])
          final_result.update(json.loads(pltfdftd.predict(law,attachment_pltf)))
          print final_result
	  return final_result
      else:
        final_result.update({'esop_id': esop_id})
    except Exception,e:
      logger.info("--error while processing pool--"+str(e)+str(esop_id))
      logger.info("Exception--inserted null values for esop--"+str(esop_id)+"--"+str(path))
    
	

def run_mdules_pool(obj):
	result = json.loads(obj.predict())
	return result

