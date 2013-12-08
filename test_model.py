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

category_counts_test= {}
MODEL_DIR = "model/"

categories = [u'entertain',u'politics',u'econonics',u'sports',u'education',u'religion',u'health']

category_counts = {
                u'entertain'  :json.load(open(MODEL_DIR+"entertain.json")),
                u'politics'   :json.load(open(MODEL_DIR+"politics.json")),
                u'econonics'  :json.load(open(MODEL_DIR+"econonics.json")),
                u'sports'     :json.load(open(MODEL_DIR+"sports.json")),
                u'education'  :json.load(open(MODEL_DIR+"education.json")),
                u'religion'   :json.load(open(MODEL_DIR+"religion.json")),
                u'health'     :json.load(open(MODEL_DIR+"health.json")),

        }

counts = json.load(open(MODEL_DIR+"data.json"))
sump = sum(c for c in counts.values())*1.0
count = 0.0
inc = 0.0
cursor = connection.cursor()
query = "SELECT * FROM `data_new` WHERE `dp` <> 'Null'"
category_counts_test = {}
cursor.execute(query)
rows = cursor.fetchall()
l = []
for row in rows :
    probability = {u'entertain':1.0,u'politics':1.0,u'econonics':1.0,u'sports':1.0,u'education':1.0,u'religion':1.0,u'health':1.0}

    cats = json.loads(row[2])
    sents = json.loads(row[4])
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
                        probability[cat] += -log((category_counts[cat][word]+1.0)/(counts[cat]+1.0))
                    except:
                        probability[cat] += -log(1.0/(counts[cat]+1.0))
            else:
                for cat in categories:
                    probability[cat] += -log(category_counts[cat][word]/(counts[cat]*1.0))

    for cat in categories:
        probability[cat] += -log(counts[cat]/sump)

    maxi= -999999
    var = u""
    for prob in  probability :
	if probability[prob] >= maxi :
		maxi = probability[prob]
		var = prob

    try :
        category_counts_test[var] +=1.0
    except :
        category_counts_test[var] = 1.0

print  counts , category_counts_test


