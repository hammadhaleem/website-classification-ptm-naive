import json
from decimal import Decimal
MODEL_DIR = 'model/'

class ModelTester(object):
	def __init__(self, k, occ, data_set, data_counts, type='dp', filename=None):
		self.k = k*1.0
		self.occ = occ
		self.type = type
		self.filename = filename
		self.data_set = data_set
		self.data_counts = data_counts
		self.cat_counts = json.load(open(MODEL_DIR+"data.json"))
		self.total_words = sum([word for word in self.cat_counts.values()])
		self.category_counts = {
                u'entertain'  :json.load(open(MODEL_DIR+"entertain.json")),
                u'politics'   :json.load(open(MODEL_DIR+"politics.json")),
                u'econonics'  :json.load(open(MODEL_DIR+"econonics.json")),
                u'sports'     :json.load(open(MODEL_DIR+"sports.json")),
                u'education'  :json.load(open(MODEL_DIR+"education.json")),
                u'religion'   :json.load(open(MODEL_DIR+"religion.json")),
                u'health'     :json.load(open(MODEL_DIR+"health.json")),
        	}
        	self.categories = [u'entertain',u'politics',u'econonics',u'sports',u'education',u'religion',u'health']

	def test(self):
		true_cases = 0
		if self.occ == 0:
                        f = open(self.filename, 'w')
                else:
                        f = open(self.filename, 'a')
		for cat, count in self.data_counts.iteritems():
			begin = int(self.occ/self.k*count)
                	end = int((self.occ+1)/self.k*count)
			for row in self.data_set[cat][begin: end]:
				cat = json.loads(row[2])[0]
				sents = json.loads(row[3])
				dp = json.loads(row[4])
				if self.type == 'dp':
					pcat = self.get_probable_category_dp(dp)
					if pcat == cat:
						true_cases += 1
				elif self.type == 'words':
					pcat = self.get_probable_category_word(sents)
					if pcat == cat:					
						true_cases += 1
				else:
					exit()
				f.write(cat+' '+pcat+'\n')
		f.close()
		print true_cases, end-begin
		return true_cases

	def get_probable_category_dp(self, dp):
		pc = {u'entertain':1.0,u'politics':1.0,u'econonics':1.0,u'sports':1.0,u'education':1.0,u'religion':1.0,u'health':1.0}
		for category in self.categories:
			pc[category] = Decimal(10**1000)
			words_in_category = sum([word_count for  word_count in self.category_counts[category].values()])
			words_count = self.total_words + words_in_category
			for w in dp:
				word = str(w)
                		if word not in self.category_counts[category]:
                    			pc[category]=pc[category]*Decimal((1.0/words_count))
                		else:
                   			pc[category]=pc[category]*Decimal(((1.0+self.category_counts[category][word])/words_count))
      		category = max(pc, key=pc.get)
      		return category

	def get_probable_category_word(self, sents):
		pc = {u'entertain':1.0,u'politics':1.0,u'econonics':1.0,u'sports':1.0,u'education':1.0,u'religion':1.0,u'health':1.0}
		for cat in self.categories:
			pc[cat] = Decimal(10**1000)
			words_in_category = sum([word_count for  word_count in self.category_counts[cat].values()])
			words_count = self.total_words + words_in_category
			for words in sents:
				for w in words:
					word = str(w)
	                		if word not in self.category_counts[cat]:
	                    			pc[cat]=pc[cat]*Decimal((1.0/words_count))
	                		else:
	                    			pc[cat]=pc[cat]*Decimal(((1.0+self.category_counts[cat][word])/words_count))
	                    			print self.category_counts[cat][word]
      		category = max(pc, key=pc.get)
		#print category      		
		return category

