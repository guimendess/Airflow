# import the libraries

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

#defining DAG arguments
default_args = {
    'owner': 'Guilherme Mendes',
    'start_date': days_ago(0),
    'email': ['guilherme@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# task definition

# task unzip_data
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar zxvf tolldata.tgz -C /home/project/airflow/dags/finalassignment/staging/',
    dag=dag,
)

# task extract_data_csv
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command='cut -d"," -f1,2,3,4 vehicle-data.csv > /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag=dag,
)

# task extract_data_tsv
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command='cut -d: -f5,6,7 tollplaza-data.tsv > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv',
    dag=dag,
)

# task extract_data_from_fixed_width
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command='cut -b 59-62,63-68 payment-data.txt > /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv',
    dag=dag,
)

# task consolidate_data
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > \
        /home/project/airflow/dags/finalassignment/staging/extracted_data.csv',
    dag=dag,
)

# task transform_data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='tr "[a-z]" "[A-Z]" < /home/project/airflow/dags/finalassignment/staging/extracted_data.csv > \
        /home/project/airflow/dags/finalassignment/staging/transformed_data.csv',
    dag=dag,
)

# task pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data