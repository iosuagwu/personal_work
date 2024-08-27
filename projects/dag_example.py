# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments
default_args = {
    'owner': 'ioswag',
    'start_date': days_ago(0),
    'email': ['example@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# define the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1)
)

# define the first task
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xzvf tolldata.tgz -C /home/project/airflow/dags/finalassignment/',
    dag=dag
)

# define the second task
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d, -f1-4 /home/project/airflow/dags/finalassignment/tolldata/vehicle-data.csv > csv_data.csv',
    dag=dag
)

# define the third task
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -f5-7 /home/project/airflow/dags/finalassignment/tolldata/tollplaza-data.tsv | tr "\t" "," > tsv_data.csv',
    dag=dag
)

# define the fourth task
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -c 59-63,64-69 /home/project/airflow/dags/finalassignment/tolldata/payment-data.txt | tr " " "," > fixed_width_data.csv',
    dag=dag
)

# define the fifth task
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv',
    dag=dag,
)

# define the fifth task
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='cut -d, -f4 extracted_data.csv > transformed_data.csv',
    dag=dag,
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
