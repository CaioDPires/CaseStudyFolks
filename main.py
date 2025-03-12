import pandas as pd
from classifier import *
from preprocess import *
import time
from database import *
from io import StringIO


#Simulacao da rota GET (imaginando que a escolha entre estruturado ou nao estruturado seja parametro da rota (na URL))
def api_get(rota:str)->str:
    #Leitura dos dados da tabela correspondentes ao parametro da rota
    if rota == '/estruturado':
        dados = pd.read_csv('data_sample/sample_estruturados.csv')

    elif rota == '/naoEstruturado':
        dados = pd.read_csv('data_sample/sample_nao_estruturados.csv')
    else:
        #Deu erro
        raise Exception('Rota invalida')
    
    return dados.to_json()

#Metodo para tentar novamente a api em caso de falha
def call_api_with_retry(url, max_retries=3, delay=2):
    for attempt in range(max_retries):
        try:
            # Make the API call
            response = api_get(url)
            return response  # If successful, return the response
        except Exception as e:
            print(f"Error on attempt {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                print("Max retries reached. Request failed.")
                return None  # Return None if all retries fail

def eh_exame_imagem(data):
    if(4070 <=int(data[0:4]) <= 4110):
        return True
    return False



def processar_nao_estruturado(df):
    df['DS_RECEITA'] = preprocess(df['DS_RECEITA'])

    df['LABEL'] = df['DS_RECEITA'].apply(regex_text)

    
    # Select only rows where LABEL == -1
    mask = df['LABEL'] == -2  
    df_not_labeled = df.loc[mask, 'DS_RECEITA'].copy()

    # Apply n-gram transformation and classification only to these rows
    if not df_not_labeled.empty:  # Ensure there are rows to process
        X = ngram_tfidf(df_not_labeled)

        y = classificar(X)

        # Update only the affected rows in the LABEL column
        df.loc[mask, 'LABEL'] = y

        # print(df[df['LABEL']==-2].shape)

        # Replace values with enum keys
        df['LABEL'] = df['LABEL'].apply(lambda x: Tipos(x).name if x in Tipos._value2member_map_ else 'UNKNOWN') 


if __name__ =='__main__':
    ##Tentar conexao a api varias vezes, senao a periodicidade ampla pode ser um problema caso haja defeito na rota
    ##USAR APENAS UMA DAS DUAS
    dados = call_api_with_retry('/estruturado')
    #dados = call_api_with_retry('/naoEstruturado')

    df = pd.read_json(StringIO(dados))

    if('CD_TUSS' in df.columns.names):
        #Transforma a df em uma lista de tuplas nomeadas e passa para o metodo que salva em base sqlite
        cria_estruturada_sqlite(list(df.itertuples(index=False)))
        
    else:
        #Processa os dados, classificando as DS_RECEITA em um dos tipos especificados no Enum em classifier.py
        #e armazenando as classificacoes na coluna 'LABEL'
        processar_nao_estruturado(df)
        #Transforma a df em uma lista de tuplas nomeadas e passa para o metodo que salva em base sqlite
        cria_nao_estruturada_sqlite(df.to_dict(orient='records'))

        ##Se quiser salvar em csv para mais facil visualizacao
        #df.to_csv('data_sample/dadosProcessados.csv', index=False)
    

    





    



    

    
    

    
    
