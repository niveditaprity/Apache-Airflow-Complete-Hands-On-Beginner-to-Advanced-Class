# 1.import modules

import airflow
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

# 2.default arguments


default_args ={
    'owner':'airflow',
    'start_date':days_ago(6),
    'depends_on_past':False,
    'email':['airflow@example.com'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

# 3. Instantiate a DAG

dag=DAG(
    'print_random_number',
    default_args=default_args,
    description='print_random_number ',
    schedule_interval=timedelta(1),
)


# 4.tasks
def print_six():
    print(6)

t1 = PythonOperator(
    task_id='print_6',
    python_callable= print_six,
    dag=dag,
)

def print_hello():
    print("Hello")

t2 = PythonOperator(
    task_id='hello',
    depends_on_past=False,
    python_callable= print_hello,
    dag=dag,
)

templated_command="""
{% for i  in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds,7) }}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param':'Parameter I passed in'},
    dag=dag,
)


# 5.setting up dependecies

t1.set_downstream(t2) #this means that t2 will depend on t1

t3.set_upstream(t1) # t3 will depends upon t1

# second way 
#t1>>t2
#t2>>t3

