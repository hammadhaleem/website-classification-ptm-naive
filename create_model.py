import json, MySQLdb
from lib.mysql import connection

def update_occurences(cat, dp):
	for k,v in dp.iteritems():
		try:
			cat[k] += v
		except:
			cat[k] = v
	return cat

categories = {
				"TOPICS" : {}, 
				"ORGS" : {},
				"EXCHANGES" : {}, 
				"COMPANIES" : {}, 
				"PLACES" : {}, 
				"PEOPLE" : {}
			}

category_counts = {
				"TOPICS" : 0, 
				"ORGS" : 0,
				"EXCHANGES" : 0, 
				"COMPANIES" : 0, 
				"PLACES" : 0, 
				"PEOPLE" : 0
			}

cursor = connection.cursor()
query = "select dp, cats from r21578 where type='train' and dp != ''"
cursor.execute(query)
cursor.scroll(0, 'absolute')
while True:
	c = cursor.fetchone()
	if not c:
		break
	# print c[0]
	dp = json.loads(c[0])
	cats = json.loads(c[1])
	for cat in cats:
		print cat
		update_occurences(categories[cat], dp)
		category_counts[cat] += 1

for cat in categories.keys():
	f = open("model/"+cat.lower()+".json", "w")
	f.write(json.dumps(categories[cat]))
	f.close()

f = open("model/data.json", "w")
f.write(json.dumps(category_counts))
f.close()