# -*- coding: utf-8
import gensim
import string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
text = open('./zakon-ob-obrazovanii-v-RF.txt', 'r', encoding='utf-8').read()
def tokenize_ru(file_text):
    tokens = word_tokenize(file_text)
    tokens = [i for i in tokens if (i not in string.punctuation)]
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])
    tokens = [i for i in tokens if (i not in stop_words)]
    tokens = [i.replace("«", "").replace("»", "") for i in tokens]
    return tokens

sentences = [tokenize_ru(sent) for sent in sent_tokenize(text, 'russian')]

model = gensim.models.Word2Vec(sentences, size=150, window=5, min_count=5, workers=4)
model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
print(model.wv.similarity('закон','образование'))
