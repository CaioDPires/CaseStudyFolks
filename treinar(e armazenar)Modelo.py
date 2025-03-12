from sklearn.model_selection import train_test_split 
from classifier import *
import warnings
from joblib import dump
warnings.filterwarnings('ignore')
import pandas



if __name__=='__main__':
    data_train = pandas.read_csv('data/data_train.csv')
    data_test = pandas.read_csv('data_sample/sample_nao_estruturados.csv')


    #Embedding (transformar o texto em algum formato aplicavel a machine learning)
    X_label_nt, vectorizer = train_ngram_tfidf(data_train.TEXTO)

    #Save classifier
    dump(vectorizer, 'modelos/vetorizador.joblib')

    y_label = data_train.LABEL
    print(X_label_nt.shape)
    X_train, X_test, y_train, y_test = train_test_split(
        X_label_nt, y_label, test_size=0.50, random_state=42)
    

    #Classifica e salva o modelo
    classifier, accuracy, y_predicted = treinar_classificador(X_train, y_train,X_test, y_test)
    print(y_predicted)

    #Save classifier
    dump(classifier, 'modelos/classificador.joblib')

    