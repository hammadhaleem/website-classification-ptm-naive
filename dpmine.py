import json, MySQLdb
from lib.dpattern import DP
from lib.mysql import connection

cursor = connection.cursor()
cursor2 = connection.cursor()
query = "SELECT `sno`,`data` FROM `data_new` WHERE 1 and `dp` is Null "
cursor.execute(query)

results = cursor.fetchall()
dp = DP(0.2)
for row in results :
	print row[0]
	dps = dp.d_patterns(json.loads(row[1]))
	query = "update `data_new` set dp = '%s' where `sno` = %s" %(json.dumps(dps).replace('\'', '\\\''), str(row[0]))
	try :
		cursor2.execute(query)
		connection.commit()
	except Exception as e:
		print e

