import json
class ModelCreator(object):
	def __init__(self, k, occ, data_set, data_counts, item_type = 'dp'):
		self.k = k*1.0
		self.occ = occ
		self.data_set = data_set
		self.item_type = item_type
		self.data_counts = data_counts
		if occ == 0:
			self.save()

	def save(self):
		print self.data_counts
		f = open('model/data.json', 'w')
		f.write(json.dumps(self.data_counts))
		f.close()

	def create(self):
		for cat,count in self.data_counts.iteritems():
			model = {}
			for i in range(len(self.data_set[cat])):
				begin = int(self.occ/self.k*count)
                		end = int((self.occ+1)/self.k*count)
				if i not in range(begin, end):
					if self.item_type == 'dp':
						dp = json.loads(self.data_set[cat][i][4])	#Use D patterns
						self.update_occurences(model, dp)
					elif self.item_type == 'words':
						sents = json.loads(self.data_set[cat][i][3])	#Use Words
						self.update_occurences_word(model, sents)
#			print model
			f = open('model/'+cat.lower()+'.json', 'w')
			f.write(json.dumps(model))
			f.close()

	def update_occurences_word(self, model, sents):
		for words in sents:
			for word in words:
				try:
					model[word] += 1
				except:
					model[word] = 1
		return model

	def update_occurences(self, cat, dp):
	    for k,v in dp.iteritems():
	        try:
	            cat[k] += v
	        except:
	            cat[k] = v
	    return cat
