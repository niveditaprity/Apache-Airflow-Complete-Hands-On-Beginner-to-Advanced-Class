from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import timedelta
def print_hello():
    return 'Hello world!'

default_args = {
    'owner': 'nivedita',
    'start_date':datetime(2022,1,6),
    'email': ['some_email@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
 }
dag = DAG('hello_world', description='Simple tutorial DAG',
          schedule_interval='@once',
          default_args = default_args, catchup=False)

from airflow import DAG
from airflow.operators.email_operator import EmailOperator

t1 = EmailOperator(
    task_id="send_mail", 
    to='nivu2211@mail.com',
    subject='Test mail',
    html_content='<p> You have got mail! <p>',
    dag=dag)


def error_function():
    raise Exception('Something wrong')
   
t2 = PythonOperator(
    task_id='failing_task',
    python_callable=error_function,
    email_on_failure=True,
    email='nivu2211@gmail.com',
    dag=dag
)
t1<<t2