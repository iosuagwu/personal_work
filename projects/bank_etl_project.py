import requests
import sqlite3
import glob 
import pandas as pd 
import numpy as np 
import xml.etree.ElementTree as ET 
from datetime import datetime 
from bs4 import BeautifulSoup

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
db_name = "Banks.db"
table_name = "Largest_banks"
log_file = "code_log.txt" 
csv_path = "exchange_rate.csv"
output_path = "/home/project/Largest_banks_data.csv"
df = pd.DataFrame(columns=['Name','MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion'])

def log_progress(message): 
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''

    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now() # get current timestamp 
    timestamp = now.strftime(timestamp_format) 
    with open(log_file,"a") as f: 
        f.write(timestamp + ':' + message + '\n')

# Bring in data from the url table into a DF
def extract(df, url):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''

    html_page = requests.get(url).text
    data = BeautifulSoup(html_page, 'html.parser')
    tables = data.find_all('table')
    rows = tables[0].find_all('tr')

    count = 0
    for row in rows:
        if count<10:
            col = row.find_all('td')
            
            if len(col)!=0:
                bank_name = col[1].find_all('a')[1]
                data_dict = {"Name": bank_name,
                            "MC_USD_Billion": float(col[2].contents[0][:-1])}
                df1 = pd.DataFrame(data_dict, index=[0])
                df = pd.concat([df,df1], ignore_index=True)
                count+=1
        else:
            break
    return df

# Transform the data to the other currency in their respective columns
def transform(df,csv_path): 
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''

    exchange_csv = pd.read_csv(csv_path)
    exchange = exchange_csv.set_index('Currency').to_dict()['Rate']

    '''Convert USD to GBP and round off to two decimals 
    1 USD is 0.8 GBP '''
    df['MC_GBP_Billion'] = [np.round(x*exchange['GBP'],2) for x in df['MC_USD_Billion']] 
 
    '''Convert USD to EUR and round off to two decimals 
    1 USD is 0.93 EUR '''
    df['MC_EUR_Billion'] = [np.round(x*exchange['EUR'],2) for x in df['MC_USD_Billion']] 

    '''Convert USD to INR and round off to two decimals 
    1 USD is 82.95 INR '''
    df['MC_INR_Billion'] = [np.round(x*exchange['INR'],2) for x in df['MC_USD_Billion']] 
    
    return df 

def load_to_csv(output_path, df):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''

    df.to_csv(output_path) 

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. ''' 

    query = sql_connection.execute(query_statement)
    print(query_statement)
    print(query.fetchall())

# Log the initialization of the ETL process 
log_progress("ETL Job Started") 
 
# Log the beginning of the Extraction process 
log_progress("Extract phase Started") 
extracted_data = extract(df,url)
print(extracted_data) 
 
# Log the completion of the Extraction process 
log_progress("Extract phase Ended") 
 
# Log the beginning of the Transformation process 
log_progress("Transform phase Started") 
transformed_data = transform(extracted_data, csv_path) 
print("Transformed Data") 
print(transformed_data) 
 
# Log the completion of the Transformation process 
log_progress("Transform phase Ended") 
 
# Log the beginning of the Loading process 
log_progress("Load phase Started") 
load_to_csv(log_file,transformed_data) 
 
# Log the completion of the Loading process 
log_progress("Load phase Ended") 

# Log the Opening of sql connection 
log_progress("SQLite3 Connection Open")
conn = sqlite3.connect(db_name)

# Log the beginning of the Loading to SQL process 
log_progress("Creation of SQL DB phase Started")
load_to_db(transformed_data,conn,table_name)

# Log the completion of the Loading to SQL process 
log_progress("Creation to SQL DB phase phase Ended") 

# Print Query Output 
log_progress("Queries Ran using SQL connector")
run_query('SELECT * FROM Largest_banks',conn)
run_query('SELECT AVG(MC_GBP_Billion) FROM Largest_banks',conn)
run_query('SELECT Name from Largest_banks LIMIT 5',conn)

# Log the Closing of SQL Connection 
log_progress("SQLite3 Connection Closed")
conn.close()

# Log the completion of the ETL process 
log_progress("ETL Job Ended") 
