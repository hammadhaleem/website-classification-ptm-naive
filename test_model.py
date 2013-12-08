import json, MySQLdb
from math import log
from operator import itemgetter
from lib.mysql import connection
from decimal import Decimal
from collections import OrderedDict

## ____Constants_____###

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
        #Assuming training data in above files

def create_matrix(l):
    dic = dict()

    for i in l :
        index = str(i[1])
        try :
            dic[index].append([i[2],i[0]])
        except :
            dic[index] = []
            dic[index].append([i[2],i[0]])
    return dic


def Get_accuracy(l):
    v=0.0
    c=0.0
    for i in l :
        if (i[0] ==i[1]):
            c+=1
        else:
            v+=1

    return (c*100)/(c+v)

def Test(rows): #Rows to test
    v = 0
    l = []
    count = 0
    counts = json.load(open(MODEL_DIR+"data.json"))
    calculated = {}

    for cat in category_counts :
        for word in category_counts[cat]:
            v += category_counts[cat][word]
    print "Total words ", v

    for category in category_counts :
        attributes = category_counts[category]
        n= 0
        for word in category_counts[category] :
            n+=  category_counts[category][word]
        calculated[category] = n

    print calculated
    for row in rows :
        count = count +1
        pc = {u'entertain':1.0,u'politics':1.0,u'econonics':1.0,u'sports':1.0,u'education':1.0,u'religion':1.0,u'health':1.0}
        id = row[1]
        cats = json.loads(row[2])
        sents = json.loads(row[3])
        dp = json.loads(row[4])
        for category in category_counts :
            n = calculated[category]
            pc[category] = Decimal(10**1000)
            #for line in sents:
            #print dp
            #dp = line
            for w in dp:
                #print word
                word = str(w)
                if word not in category_counts[category]:
                    pc[category]=pc[category]*Decimal((1.0/(n+v)))
                else:
                    pc[category]=pc[category]*Decimal(((1.0+category_counts[category][word])/(n+v)))
        p=0
        Category=u'Unable to decide'
        for category in categories:
            if p<pc[category]:
                Category=category
                p=pc[category]
        for i in cats:
            l.append([Category , i , id ] )
        if (count % 200 == 0 ):
            x =create_matrix(l)
            print "Tested on" , count ,"Accuracy" , Get_accuracy(l) 
            f=open("choas","w")
            f.write(json.dumps(x))
            f.close()

    x =create_matrix(l)
    f=open("choas","w")
    f.write(json.dumps(x))
    f.close()



cursor = connection.cursor()
query ="SELECT * FROM `data_new` WHERE 1 "
cursor.execute(query)
rows = cursor.fetchall()
Test(rows)
