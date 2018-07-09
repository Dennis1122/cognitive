import myconfig
from datetime import datetime
from loger import logger
import time
class Error_Handler:
  
  def mysql_insert_error(self,program_name,error_code,errro_msg):
    
    con_error = mdb.connect(myconfig.mysql_server, myconfig.mysql_username_error,
						   myconfig.mysql_pass_error, myconfig.mysql_db_error)
    cursor_error = con_error.cursor()
    add_value = ("INSERT INTO mlins.vapplication_error_log_TCS"
				 "(VENDOR_ID,PROGRAM_NAME,ERROR_CODE,ERROR_DATE,ERROR_MSG)"
				 "VALUES (%s,%s,%s,%s,%s)")
    now = time.strftime('%Y-%m-%d')
    
    data_value = (int(myconfig.vendor_id),program_name,int(error_code),now,errro_msg)
    try:
      cursor_error.execute(add_value, data_value)
      #print "success"
    except Exception, e:
      #print str(e)
      logger.error("An error has occurred"+str(e))
      con_error.rollback()
    else:
      con_error.commit()
    cursor_error.close()
    con_error.close()
