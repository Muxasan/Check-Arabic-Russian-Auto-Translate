from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
import string
import gensim
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import sys

ma = MA()
st = PST()
wt = WPT()

text1 = """Каждый человек имеет право на образование.
Образование должно быть бесплатным, по меньшей мере,
в том, что касается начального и общего образования.
Начальное образование должно быть обязательным.
Техническое и профессиональное образование должно быть общедоступным,
и высшее образование должно быть одинаково доступным для всех
на основе способностей каждого."""
text2 = """Каждый человек имеет право на образование.
Образование должно быть, по крайней мере, на ранних этапах,
и по крайней мере базовое, начальное образование должно быть обязательным,
техническое и профессиональное образование должно быть обобщено,
а доступ к высшему образованию должен быть обеспечен наравне со всеми и
на основе компетенции."""

sys.stdout = open('Result2.txt','w')

text = open('./zakon-ob-obrazovanii-v-RF.txt', 'r', encoding='utf-8').read()
def tokenize_ru(file_text):
    tokens = word_tokenize(file_text)
    tokens = [i for i in tokens if (i not in string.punctuation)]
    tokens = [i for i in tokens1 if ( ma.parse(i)[0].tag.POS not in functors_pos )]
    tokens = [i.replace("«", "").replace("»", "") for i in tokens]
    return tokens

tokens1 = wt.tokenize(text1)       
tokens2 = wt.tokenize(text2)
functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}                     # Удаляем пунктуацию
tokens1 = [i for i in tokens1 if ( i not in string.punctuation )]
tokens2 = [i for i in tokens2 if ( i not in string.punctuation )]
tokens1 = [i for i in tokens1 if ( ma.parse(i)[0].tag.POS not in functors_pos )]   
tokens2 = [i for i in tokens2 if ( ma.parse(i)[0].tag.POS not in functors_pos )]
i = 0
while i<len(tokens1):                     # Переводим в нижний регистр
    tokens1[i] = tokens1[i].lower()
    i = i + 1
i = 0
while i<len(tokens2):
    tokens2[i] = tokens2[i].lower()
    i = i + 1

sentences = [tokenize_ru(sent) for sent in sent_tokenize(text, 'russian')]
model = gensim.models.Word2Vec(sentences, size=500, window=5, min_count=1, workers=4)
model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)
i = 0
j = 0
while i<min(len(tokens1),len(tokens2)):
    result = model.wv.similarity(tokens1[i],tokens2[i])
    if tokens1[i] == tokens2[i]:
        i = i + 1
        j = j + 1
    else:
        if result < 0.4:
            print(tokens1[j],'-',tokens2[i],result,'Неправильный перевод, отсутствует слово')
            if tokens1[j+1] == tokens2[i]:
                j = j + 1
            else:
                i = i + 1
        if result > 0.4 and result < 0.7:
            print(tokens1[j],'-',tokens2[i],result,'Неправильный перевод, неверный перевод')
        if result > 0.70 and result < 1:
            print(tokens1[j],'-',tokens2[i],result,'Неправильный перевод, корректировка')
        i = i + 1
        j = j + 1

print(tokens1)
print(tokens2)
sys.stdout.close()
