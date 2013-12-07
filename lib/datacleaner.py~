import nltk
from nltk import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

class DataClean:
    def __init__(self,text):
        lmtzr = WordNetLemmatizer()
        porter_stem = PorterStemmer()
        wordnet_tag ={'NN':'n','JJ':'a','VB':'v','RB':'r'}
        data = text.lower()
        tokens = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokens)
        word_list = []
        for t in tagged:
            try:
                word_list.append(lmtzr.lemmatize(t[0],wordnet_tag[t[1][:2]]))
            except:
                word_list.append(porter_stem.stem_word(t[0]))
        self.filtered_words = [w for w in word_list if not w in stopwords.words('english')]

    def getData(self):
        return self.filtered_words