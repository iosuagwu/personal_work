# Import libraries required for connecting to mysql
import mysql.connector
# Import libraries required for connecting to DB2 or PostgreSql
import psycopg2
# Connect to MySQL
connection = mysql.connector.connect(user='', password='',host='',database='')
# Connect to DB2 or PostgreSql
dsn_hostname = #
dsn_user=# e.g. "abc12345"
dsn_pwd =# e.g. "7dBZ3wWt9XN6$o0J"
dsn_port =# e.g. "50000" 
dsn_database =# i.e. "BLUDB"

conn = psycopg2.connect(
   database=dsn_database, 
   user=dsn_user,
   password=dsn_pwd,
   host=dsn_hostname, 
   port= dsn_port
)

# Find out the last rowid from DB2 data warehouse or PostgreSql data warehouse
# The function get_last_rowid must return the last rowid of the table sales_data on the IBM DB2 database or PostgreSql.

def get_last_rowid():
    cursor = conn.cursor()
    cursor.execute('SELECT max(rowid) from "sales_data";')
    rows = cursor.fetchall()
    conn.commit()
    last_rowid = rows[0]
    return last_rowid


last_row_id = get_last_rowid()
print("Last row id on production datawarehouse = ", last_row_id)

# List out all records in MySQL database with rowid greater than the one on the Data warehouse
# The function get_latest_records must return a list of all records that have a rowid greater than the last_row_id in the sales_data table in the sales database on the MySQL staging data warehouse.

def get_latest_records(rowid):
    cursor = connection.cursor()
    new_records = []
    SQL = "SELECT * FROM sales_data where rowid> {};".format(rowid)
    cursor.execute(SQL)
    for row in cursor.fetchall():
        new_records.append(row)
    return new_records	

new_records = get_latest_records(last_row_id)

print("New rows on staging datawarehouse = ", len(new_records))

# Insert the additional records from MySQL into DB2 or PostgreSql data warehouse.
# The function insert_records must insert all the records passed to it into the sales_data table in IBM DB2 database or PostgreSql.

def insert_records(records):
    cursor = conn.cursor()
    for row in records:
        SQL="INSERT INTO sales_data(rowid,product_id,customer_id,quantity,price,timestamp) values(%s,%s,%s,%s,%s,%s);" 
        cursor.execute(SQL,row)
        conn.commit()

insert_records(new_records)
print("New rows inserted into production datawarehouse = ", len(new_records))

# disconnect from mysql warehouse
connection.close()
# disconnect from DB2 or PostgreSql data warehouse 
conn.close()
# End of program
