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

categories = ['entertain','politics','econonics','sports','education','religion','health']

category_counts = {
                'entertain'  :json.load(open(MODEL_DIR+"entertain.json")),
   				'politics'   :json.load(open(MODEL_DIR+"politics.json")), 
    			'econonics'  :json.load(open(MODEL_DIR+"econonics.json")),
    			'sports'     :json.load(open(MODEL_DIR+"sports.json")),
    			'education'  :json.load(open(MODEL_DIR+"education.json")),
    			'religion'   :json.load(open(MODEL_DIR+"religion.json")),
    			'health'     :json.load(open(MODEL_DIR+"health.json")),

        }

counts = json.load(open(MODEL_DIR+"data.json"))
sump = sum(c for c in counts.values())*1.0
count = 0.0
inc = 0.0
cursor = connection.cursor()
query = "SELECT * FROM `data_new` WHERE `dp` <> 'Null' "
cursor.execute(query)
rows = cursor.fetchall()
for row in rows :
    probability = {'entertain':1.0,'politics':1.0,'econonics':1.0,'sports':1.0,'education':1.0,'religion':1.0,'health':1.0,}
    
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


    maxi= -9999
    cats = json.loads(row[2])
    for i in probability :
    	if (probability[i] >=  maxi) :
    		maxi = probability[i]
    		var = i

    for i in cats :
    	if i == var :
    		inc = inc +1 
    		break
    count =count + 1
    print (inc/count)
    print cats