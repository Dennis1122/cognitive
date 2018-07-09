import MySQLdb as mdb
import myconfig
import time

mysql_server = 'sopmldev.cksvayyfolrw.us-east-1.rds.amazonaws.com'
mysql_username = 'sopmluser_tcs'
mysql_pass = 'XiGBHaXQ'
mysql_db = 'arrowml'

def mySQL_query():
	data = []
	con = mdb.connect(mysql_server, mysql_username,
						   mysql_pass, mysql_db);
	cursor = con.cursor()
	esop_id = 0
	
	try:
		cursor.execute('SELECT MAX(ESOP_ID) FROM arrowml.Vsop_extract_ml_TCS')
		esop_id = cursor.fetchone()[0]
		if esop_id == None:
		  esop_id = 0
	except Exception, e:
		esop_id = 0
	
	try:
		query_select = "SELECT ESOP_ID, DOC_URL FROM arrowml.Vesop_inbox_ml WHERE ESOP_ID > %s AND DOC_URL IS NOT NULL LIMIT 30"
		cursor.execute(query_select,(esop_id,))
		data = cursor.fetchall()

	except Exception, e:
		print "An error has occurred"+str(e)
	
	cursor.close()
	con.close()
	return data