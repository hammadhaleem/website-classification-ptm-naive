import os
from lxml import etree
import lxml
import lxml.html

def GetDirList(cur_dir, list):
  for root, dirs, files in os.walk(cur_dir):
      for name in files:
        if name.endswith('.xml'):
          list.append(os.path.join(root, name))
      for name in dirs:
        GetDirList(os.path.join(root, name),list)
  return list




list =[]
list = GetDirList(os.getcwd(),list)
count = 0
dic = {} 

f= open('file','w')
f.write(str(list))
'''
l= str(f.read())
l.replace("'",'').replace('[','').replace(']','').replace(' ','')
list= l.split(',')
'''
f.close()
for path in list :
	print path + "\t"+str(count)
	count =count +1
	f = open(path , 'r')
	text = str(f.read())
	doc = lxml.html.document_fromstring(text)
	txt2 = doc.xpath("//codes[@class='bip:topics:1.0']/code/@code")
	for i in txt2 :
		try :
			dic[i]=dic[i]+1
		except :
			dic[i]=1
	if (count % 500) == 0 :
		f= open('out','w')
		for j in dic :
			print j, dic[j]  
			k = str(j)+ " : " +str(dic[j]) + "\n"
			f.write(str(k))
		f.close() 


f= open('out','w')
for j in dic :
	print j, dic[j]  
	k = str(j)+ " : " +str(dic[j]) + "\n"
	f.write(str(k))
f.close()   
























