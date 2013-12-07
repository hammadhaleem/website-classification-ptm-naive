import json, MySQLdb
from math import log
from operator import itemgetter
from lib.mysql import connection

def update_occurences(cat, dp):
	for k,v in dp.iteritems():
		try:
			cat[k] += v
		except:
			cat[k] = v
	return cat

MODEL_DIR = "model/"

categories = ["TOPICS", "ORGS", "EXCHANGES", "PLACES", "PEOPLE"]

category_counts = {
				"TOPICS" : json.load(open(MODEL_DIR+"topics.json")), 
				"ORGS" : json.load(open(MODEL_DIR+"orgs.json")),
				"EXCHANGES" : json.load(open(MODEL_DIR+"exchanges.json")), 
				"PLACES" : json.load(open(MODEL_DIR+"places.json")), 
				"PEOPLE" : json.load(open(MODEL_DIR+"people.json"))
		}

counts = json.load(open(MODEL_DIR+"data.json"))

sump = sum(c for c in counts.values())*1.0

cursor = connection.cursor()
query = "select cats, data from r21578 where type='test'"
cursor.execute(query)
cursor.scroll(0, 'absolute')
while True:
	c = cursor.fetchone()
	if not c:
		break
	# print c[0]
	probability = {"TOPICS":1, "ORGS":1, "EXCHANGES":1, "PLACES":1, "PEOPLE":1}
	cats = json.loads(c[0])
	sents = json.loads(c[1])
	for words in sents:
		for word in words:
			foureir_applied = False
			for cat in categories:
				if not category_counts[cat].has_key(word):
					foureir_applied = True
					break
			if foureir_applied:
				for cat in categories:
					try:
						probability[cat] *= -log((category_counts[cat][word]+1.0)/(counts[cat]+1.0))
					except:
						probability[cat] *= -log(1.0/(counts[cat]+1.0))
			else:
				for cat in categories:
					probability[cat] *= -log(category_counts[cat][word]/(counts[cat]*1.0))

	for cat in categories:
		probability[cat] *= -log(counts[cat]/sump)

	src = sorted(probability.keys(), key=itemgetter(1))
	src.reverse()
	print src
	print cats
