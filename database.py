import csv
from datetime import datetime
import sqlite3

def cria_nao_estruturada_sqlite(dictionary):
    try:
        consultation_info = []
        for values in dictionary:
            dt = datetime.strptime(values['DATA'], '%Y-%m-%d')
            
            # Convert the datetime object to a date object
            date_obj = dt.date()

            consultation_info.append((date_obj, values['TEL'], values['CPF'], values['SOLICITANTE'], values['DS_RECEITA'], values['LABEL']))
            #print(consultation_info)

        # Connect to SQLite
        sqliteConnection = sqlite3.connect('hospitalDB.db')
        cursor = sqliteConnection.cursor()
    
        # Create student table
        cursor.execute("""create table if not exists NaoEstruturado(
        Data text,
        Telefone text,
        CPF text,
        Nome text,
        DsReceita text,
        Tipo text,
        PRIMARY KEY(Data, CPF, DsReceita));""")
        sqliteConnection.commit()
        # Insert data into table
        cursor.executemany(
            "INSERT OR REPLACE into NaoEstruturado (Data, Telefone, CPF, Nome, DsReceita, Tipo) VALUES (?, ?, ?, ?, ?, ?);", consultation_info)
    
        # Commit work and close connection
        sqliteConnection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')


def cria_estruturada_sqlite(dictionary):
    try:
        consultation_info = []
        for values in dictionary:
            dt = datetime.strptime(values['DATA'], '%Y-%m-%d')
            
            # Convert the datetime object to a date object
            date_obj = dt.date()

            consultation_info.append((date_obj, values['TEL'], values['CPF'], values['SOLICITANTE'], values['CD_TUSS'], values['DS_RECEITA']))
            #print(consultation_info)

                
        # Connect to SQLite
        sqliteConnection = sqlite3.connect('hospitalDB.db')
        cursor = sqliteConnection.cursor()
    
        # Create student table
        cursor.execute("""create table if not exists Estruturado(
        Data text,
        Telefone text,
        CPF text,
        Nome text,
        CodigoTUSS text,
        DsReceita text,
        PRIMARY KEY(Data, CPF, CodigoTUSS));""")

        sqliteConnection.commit()
        
        # Insert data into table
        cursor.executemany(
            "insert into Estruturado (Data, Telefone, CPF, Nome, CodigoTUSS , DsReceita) VALUES (?, ?, ?, ?, ?, ?);", consultation_info)
    
        # Commit work and close connection
        sqliteConnection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')



def cria_nao_estruturada_sqlite_do_csv():
    try:
        # Import csv and extract data
        with open('data_sample/dadosProcessados.csv', 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            # Parse the datetime string (adjust the format to match your CSV)
            consultation_info = []
            for i in dr:
                dt = datetime.strptime(i['DATA'], '%Y-%m-%d')
                
                # Convert the datetime object to a date object
                date_obj = dt.date()

                consultation_info.append((date_obj, i['TEL'], i['CPF'], i['SOLICITANTE'], i['DS_RECEITA'], i['LABEL']))
                #print(consultation_info)
    
        # Connect to SQLite
        sqliteConnection = sqlite3.connect('hospitalDB.db')
        cursor = sqliteConnection.cursor()
    
        # Create student table
        cursor.execute("""create table if not exists NaoEstruturado(
        Data text,
        Telefone text,
        CPF text,
        Nome text,
        DsReceita text,
        Tipo text,
        PRIMARY KEY(Data, CPF, DsReceita));""")
    
        # Insert data into table
        cursor.executemany(
            "insert into NaoEstruturado (Data, Telefone, CPF, Nome, DsReceita, Tipo) VALUES (?, ?, ?, ?, ?, ?);", consultation_info)
    
    
        # Commit work and close connection
        sqliteConnection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')
