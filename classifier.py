import re
from matplotlib import pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load
import numpy as np

from enum import Enum
class Tipos(Enum):
    Invalido = -1
    Receita = 0
    Exame = 1
    Encaminhamento = 2
    Outros = 3


##0 Receita, 

#Tokenizador simples
def ngram_tfidf(X):
    model = load('modelos/vetorizador.joblib')
    X = model.transform(X)
    return X


def train_ngram_tfidf(X, model=None):
    if model == None:
        kwargs = {
            'ngram_range': (1, 2), 
            'dtype': 'int32',
            'decode_error': 'replace',
            'analyzer': 'word',
            'min_df': 2,
        }
        model = TfidfVectorizer(**kwargs)
        X = model.fit_transform(X)
        
    else:
        X = model.transform(X)
    return X, model


def treinar_classificador(X_train, y_train, X_test, y_test):
    """
    Realiza a classificação e calcula a acurácia.

    Parâmetros:
    - X_train: Dados de treinamento (features).
    - y_train: Rótulos de treinamento.
    - X_test: Dados de teste (features).
    - y_test: Rótulos de teste.
    - cls: Classificador a ser treinado.

    Retorna:
    - classifier: Classificador treinado.
    - accuracy: Acurácia do classificador no conjunto de teste.
    - y_pred: Classes preditas.
    """
    # Treina o classificador
    #Classificador
    classifier= RandomForestClassifier(n_estimators=50, random_state=1)
    
    classifier.fit(X_train, y_train)

    # Faz as previsões
    y_pred = classifier.predict(X_test)

    # Calcula a acurácia
    accuracy = accuracy_score(y_test, y_pred)

    print(f'Acurácia: {accuracy:.2f}')

    return classifier, accuracy, y_pred


def classificar(X):
    model = load('modelos/classificador.joblib')
    return model.predict(X)

def classificar_prob(X):
    model = load('modelos/classificador.joblib')
    proba = model.predict_proba(X)
    confidence = np.max(proba, axis=1)
    threshold = 0.85  # Adjust based on your data

    # Flag low-confidence predictions as "unknown"
    y_pred = [model.classes_[np.argmax(p)] if conf > threshold else -2 for p, conf in zip(proba, confidence)]
    return y_pred


def regex_text(text):
    # Textos invalidos
    if not text or text.lower() == "none":
        return Tipos.Invalido.value
    
    #Padroes regex de notas, orientacoes, relatorios, etc.
    notes_patterns = [r"(orientacoes)",r"(informacao paciente)",r"(obstipante)",r"(relatorio medico)"]
    for pattern in notes_patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if match:
            return Tipos.Outros.value
        
    #Padroes de receita
    prescription_patterns = [r"^(uso oral [a-zA-z]* \d* mg)", r"^(uso [a-zA-z]* [a-zA-z]* \d*mg)", r"^(uso [a-zA-z]* [a-zA-z]* \d* comp)",
                             r"^(uso [a-zA-z]* [a-zA-z]* \d* fr)", r"^(uso [a-zA-z]* \d*. [a-zA-z]* \d* fr)", r"^(uso [a-zA-z]* \d* [a-zA-z]* \d*)",
                             r"^(uso [a-zA-z]* \d* [a-zA-z]* \d*mg)", r"^(uso [a-zA-z]* [a-zA-z]* \d* gota)" r"^([a-zA-Z]* \d*ng [a-zA-Z]* \d* vd)",
                             r"(^\d*. [a-zA-Z]* \d* [a-zA-Z]* \d* cx [a-zA-Z]* \d comp)", r"(^\d*. [a-zA-Z]* \d* [a-zA-Z]* \d*cx [a-zA-Z]* \d comp)",
                             r"tomar\s\d+\scp"
                             ]
    for pattern in prescription_patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if match:
            return Tipos.Receita.value
    
    #Padroes de solicitacao de exame
    exam_patterns = [r"^solicito\s+exame", r"\bsolicito(:|\s*(usg|rx|ecg))", r"\b\w*oscopia", r"exames",
                     r"ao laboratorio", r"\bcoleta\b", r"(eletrocardiograma)"]
    for pattern in exam_patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if match:
            return Tipos.Exame.value
        
    #Padroes de encaminhamento a profissionais
    referral_patterns = [r"^(encaminho (a|ao).*)", r"^a fisioterapia", r"(?=.*\b(fisioterapia|fisioterapeuta)\b)(?=.*\bsessoes\b).*"]
    for pattern in referral_patterns:
        match = re.search(pattern, text, flags=re.I | re.M)
        if match:
            return Tipos.Encaminhamento.value
        
    return -2
    


