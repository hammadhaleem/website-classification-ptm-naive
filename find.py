import json, MySQLdb
from lib.mysql import connection


cursor = connection.cursor()
l_ = '["education"]'
query = "SELECT * FROM `data_new` WHERE `dp` <> 'Null'  and `topic` = '"+str(l_)+"'"
cursor.execute(query)
data = cursor.fetchall ()
count  = 0
for row in data :
    dp = json.loads(row[4])
    flag = 0 
    for i in dp :
	flag = flag+1 
    if count < 150 :
	cu = connection.cursor()
    	q = "DELETE FROM `data_new` WHERE `sno` ='"+str(row[0])+ "' ; "
	count += 1 	 
	try :
    		cu.execute(q)
        	connection.commit()
	except :
		print "error "
	

print count 
