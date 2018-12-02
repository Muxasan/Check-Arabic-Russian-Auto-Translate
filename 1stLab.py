from pymorphy2 import MorphAnalyzer as MA
from nltk.tokenize import PunktSentenceTokenizer as PST
from nltk.tokenize import WordPunctTokenizer as WPT
import string
from nltk.corpus import stopwords

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

tokens1 = wt.tokenize(text1)
tokens2 = wt.tokenize(text2)
tokens1 = [i for i in tokens1 if ( i not in string.punctuation )]
tokens2 = [i for i in tokens2 if ( i not in string.punctuation )]
print(tokens1)
print(tokens2)
    
