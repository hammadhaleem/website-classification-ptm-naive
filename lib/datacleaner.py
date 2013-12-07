class DataClean:
	def __init__(self,text):
		s1='!@#$)(*&^%~`*!{}][;":/.,?><_-+='
		
		for ch in s1: 			   
			if ch in text :
				text=text.replace(ch," ")

		text = text.lower()
	        tokens = nltk.word_tokenize(text)
	        tagged = nltk.pos_tag(tokens)
	        word_list = []	
		
	        for t in tagged:
	            try:
			if t[0] in stopwords.words('english'):
				pass
			else:	
				x =lmtzr.lemmatize(t[0],wordnet_tag[t[1][:2]])
				if len(x) > 1 : 
	                		word_list.append(x)
	            except:
			if t[0] in stopwords.words('english'):
				pass
			else:
				v =porter_stem.stem_word(t[0])
				if len(v) > 1 :
	                		word_list.append(v)
		self.filtered_words = word_list

		
	def GetData(self):
        	return self.filtered_words

