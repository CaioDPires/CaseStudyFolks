import re
import unidecode
import pandas as pd
from nltk.corpus import stopwords

def symbol_decimal_separator(data):
    for i, text in enumerate(data):
        x = []
        for string in text.split():
            m = re.search("\d+\,\d*", string)
            if m != None:
                string = string.replace(',', '.')
            x.append(string)
        data.values[i] = ' '.join(x)
    return data

def normalize_dosage(data):
    for i, text in enumerate(data):
        # Add a space between numbers and units (e.g., "50mg" -> "50 mg")
        text = re.sub(r'(\d+)(mg|g|ml|kg|%)', r'\1 \2', text, flags=re.IGNORECASE)
        data.values[i] = text


def remove_stopwords(data):
    stop_words = stopwords.words('portuguese')
    for i, text in enumerate(data):
        text = ' '.join([word for word in text.split() if word not in stop_words])
        data.values[i] = text
    return data

#x / para x
def replace_frequency(data):
    for i, text in enumerate(data):
        text = text.replace('x /', 'x')
        data.values[i] = text
    return data


def remove_spaces(data):
    for i, text in enumerate(data):
        data.values[i] = ' '.join(text.split())
    return data


def remove_accents(data):
    for i, text in enumerate(data):
        data.values[i] = unidecode.unidecode(text)
    return data


def remove_punctuation(data):
    exc_list = '"#\'*-=@[\\]_{|}`^~'
    table_ = str.maketrans(exc_list, ' '*len(exc_list))
    
    for i, text in enumerate(data):
        text = ' '.join(text.translate(table_).split())
        text = re.sub('\.{2,}', ' ', text)
        data.values[i] = text
    return data


def lowercase(data):
    data = data.str.lower()
    return data


#Recebe um df e o nome da coluna
def preprocess(data: pd.Series)->pd.Series:
    data = data.astype(str).fillna("")
    
    data = remove_accents(data)

    data = remove_punctuation(data)

    data = symbol_decimal_separator(data)

    data = remove_spaces(data)

    data = lowercase(data)

    data = replace_frequency(data)

    data.replace("none", "", inplace=True)

    return data

if __name__ == '__main__':
    data = pd.read_csv('data_sample/sample_nao_estruturados.csv')
    data['DS_RECEITA'] = preprocess(data['DS_RECEITA'])

