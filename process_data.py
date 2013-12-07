import os
import lxml.html
from nltk import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from string import maketrans 

import os, json, MySQLdb
from lib.mysql import connection
from lib.datacleaner import DataClean

#Preprocess the RCV1 Dataset 
#Globals
lmtzr = WordNetLemmatizer()
porter_stem = PorterStemmer()
wordnet_tag ={'NN':'n','JJ':'a','VB':'v','RB':'r'}

topics = {
	'entertain' : ['ENT12','GENT','GFAS'],
	'politics' 	: ['1POL','G12','GPOL'],
	'econonics' : ['2ECO','E11','E12','ECAT'],
	'sports'	: ['3SPO','GSPO'],
	'education'	: ['G113','GEDU','C23','GSCI'],	
	'religion'	: ['GREL'],	
	'health'	: ['G111','GHEA'],
	}

print "Init"


def addslashes(s):
	l = ["\\", '"', "'", "\0", ]
	for i in l:
		if i in s:
			s = s.replace(i, '\\'+i)
	return s
def dbwrite(p,x1,x2):
	try :
		connection = MySQLdb.connect('localhost', 'root', 'kgggdkp2692', 'mining')
	except Exception as e :
		connection =None
		print "Unable to connect   :" + str(e)

	x = connection.cursor()
	try:
		q= "INSERT INTO `data_new` (`path`,`topic`,`data`) VALUES ('"+addslashes(str(p))+"','"+json.dumps(x1).replace('\'', '\\\'')+"','"+json.dumps(x2).replace('\'', '\\\'')+"')"
		x.execute(q)
		connection.commit()
	except Exception as e :
		print e
		connection.rollback()
		connection.close()



def GetDirList(cur_dir, list):
  for root, dirs, files in os.walk(cur_dir):
      for name in files:
        if name.endswith('.xml'):
          list.append(os.path.join(root, name))
      for name in dirs:
        GetDirList(os.path.join(root, name),list)
  return list


list =[]
list.sort()
list = GetDirList(os.getcwd(),list)
count = 0
#list.sort(reverse=True)

print "Counted..Processing "
for path in list :
	count =count +1
	try:
		
		try : 
			f = open(path , 'r')
			text = str(f.read())
		except Exception as E :
			print "FILE ERROR" , E 
		finally :
			f.close()
			#os.remove(path)
			list.remove(path)

		doc = lxml.html.document_fromstring(text)
		txt2 = doc.xpath("//codes[@class='bip:topics:1.0']/code/@code")
		flag = 0 
		id1 = doc.xpath("//newsitem/@itemid")
		
		top = []
		for i in txt2 :
			for k in topics:
				if i in topics[k]:
					flag =1
					if k in top :
						pass
					else : 
						top.append(k)
		if flag == 1 :
			txt1 = doc.xpath("//p/text()")
			lis = [] 
			for i in txt1 :
				l=DataClean(i).GetData()
				lis.append(l)

			dbwrite(id1[0],top,lis) 
			print top ,count ,len(list)
		if ( count % 1000 == 0 ):
			print count , len(list)
	except Exception as e :
		print e , path ,str(count)
	
		






































	
