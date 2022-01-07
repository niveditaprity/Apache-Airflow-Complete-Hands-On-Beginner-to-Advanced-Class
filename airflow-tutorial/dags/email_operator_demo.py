import airflow
from datetime import timedelta
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator



default_args = {
        'email': ['some_email@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
        }    


dag_email = DAG(
    dag_id = 'emailoperator_demo',
    default_args=default_args,
    schedule_interval=timedelta(1), 
    dagrun_timeout=timedelta(minutes=60),
    description='use case of email operator in airflow',
    start_date = airflow.utils.dates.days_ago(1))


def start_task():
    print("task started")


start_task = PythonOperator(
    task_id='executetask',
    python_callable=start_task,
    dag=dag_email)
    
send_email = EmailOperator(
    task_id='send_email',
    to='nivu2211@gmail.com',
    subject='ingestion complete',
    html_content="Date: {{ ds }}",
    dag=dag_email)


send_email.set_upstream(start_task)
