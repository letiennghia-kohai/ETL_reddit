import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipelines.reddit_pipeline import reddit_pipeline
from pipelines.mysql_pipeline import load_data_to_mysql

default_args = {
    'owner': 'Nghia LT',
    'start_date': datetime(2023, 10, 22)
}

file_postfix = datetime.now().strftime("%Y%m%d")
file_name = f'reddit_{file_postfix}'

dag = DAG(
    dag_id='etl_reddit_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['reddit', 'etl', 'pipeline']
)

# extraction from reddit
extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs={
        'file_name': file_name,
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

# load to mysql
load_mysql = PythonOperator(
    task_id='load_to_mysql',
    python_callable=load_data_to_mysql,
    op_kwargs={
        'table_name': 'reddit_data'
    },
    dag=dag
)

extract >> load_mysql
