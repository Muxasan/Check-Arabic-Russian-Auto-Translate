from pymorphy2 import MorphAnalyzer as MA

from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
import string
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim

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

tokens1 = wt.tokenize(text1)        # Разбиваем на слова
tokens2 = wt.tokenize(text2)
functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}                     # Удаляем пунктуацию
tokens1 = [i for i in tokens1 if ( i not in string.punctuation )]
tokens2 = [i for i in tokens2 if ( i not in string.punctuation )]
tokens1 = [i for i in tokens1 if ( ma.parse(i)[0].tag.POS not in functors_pos )]   # Удаляем служебные части речи
tokens2 = [i for i in tokens2 if ( ma.parse(i)[0].tag.POS not in functors_pos )]
i = 0
while i<len(tokens1):                     # Переводим в нижний регистр
    tokens1[i] = tokens1[i].lower()
    i = i + 1
i = 0
while i<len(tokens2):
    tokens2[i] = tokens2[i].lower()
    i = i + 1
i = 0
w2v_fpath = "all.norm-sz100-w10-cb0-it1-min100.w2v"
w2v = gensim.models.KeyedVectors.load_word2vec_format(w2v_fpath, binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)
while i<min(len(tokens1),len(tokens2)):
    if tokens1[i] == tokens2[i]:
        i = i + 1
    else:
        result = w2v.similarity(tokens1[i],tokens2[i])
        print(tokens1[i],' ',tokens2[i],' ',result)
        if result < 0.35:
            print(tokens1[i],'-',tokens2[i],'Неправильный перевод, возможно неверное слово')
        else:
            if result > 0.35 and result < 0.7:
                print(tokens1[i],'-',tokens2[i],'Неправильный перевод, корректировка')
            else:
                print(tokens1[i],'-',tokens2[i],'Неправильный перевод, неверный падеж')
        i = i + 1

print(tokens1)
print(tokens2)

