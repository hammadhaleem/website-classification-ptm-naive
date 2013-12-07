from cleaning import *
class DataClean:
	def __init__(self,text):
		
		words=seperateWords(text)
		words=convertToLower(words) # convert words to lowercase
		words=applyStemming(words)
		words=removeStopWords(words) # remove stop words
		words=removeSmallWords(words)
		self.filtered_words = words
		
	def GetData(self):
        	return self.filtered_words

