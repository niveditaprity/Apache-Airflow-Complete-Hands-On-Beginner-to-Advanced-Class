from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

#dag = DAG('core_concepts',schedule_interval='@daily',catchup=False)

from random import seed,random

from airflow.utils.helpers import chain,cross_downstream
#default_args = {'owner':'Admin','start_date':days_ago(1)}
#op = Op(dag=dag)
default_args = {
    'owner': 'Admin',
    'start_date': days_ago(2),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

def alg_1():
    print('\nHello alg1')
    print('\nHFinshed alg1')

def alg_2():
    print('\nHello alg2')
    print('\nHFinshed alg2')

def alg_3():
    print('\nHello alg3')
    print('\nHFinshed alg3')


with DAG('my_test', description='my_test description', catchup=False, default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    python_task_1 = PythonOperator(task_id='my_task_1', python_callable=alg_1)
    python_task_2 = PythonOperator(task_id='my_task_2', python_callable=alg_2)
    python_task_3 = PythonOperator(task_id='my_task_3', python_callable=alg_3)

    python_task_1 >> python_task_2
    python_task_2 >> python_task_3
#bash_task.set_downstream(python_task)

#op1 >> op2 >> op3 >> op4

#chain(op1,op2,op3,op4)
#cross_downstream([op1,op2],[op3,op4])

#[op1,op2] >>op3

#[op1,op2] >> op4


