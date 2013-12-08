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
    'entertain'  :{},
    'politics'   :{},
    'econonics'  :{},
    'sports'     :{},
    'education'  :{},
    'religion'   :{},
    'health'     :{},
            }

category_counts= {
    'entertain'  :0,
    'politics'   :0,
    'econonics'  :0,
    'sports'     :0,
    'education'  :0,
    'religion'   :0,
    'health'     :0,
    }

cursor = connection.cursor()
query = "SELECT * FROM `data_new` WHERE `dp` <> 'Null' "
cursor.execute(query)
data = cursor.fetchall ()
count  = 0
for row in data :
    cats = json.loads(row[2])
    dp = json.loads(row[4])
    count = count + 1
    print count
    c= 0
    for cat in cats:
        print cat
        c+=1
    if c == 1 :
        update_occurences(categories[cat], dp)
        category_counts[cat] += 1


for cat in categories.keys():
    f = open("model/"+cat.lower()+".json", "w")
    f.write(json.dumps(categories[cat]))
    f.close()

f = open("model/data.json", "w")
f.write(json.dumps(category_counts))
f.close()
