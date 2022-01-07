# 1.import modules

import airflow
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator

# 2.default arguments


default_args ={
    'owner':'airflow',
    'start_date':days_ago(4),
    'depends_on_past':False,
    'email':['airflow@example.com'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

# 3. Instantiate a DAG

dag=DAG(
    'new_description',
    default_args=default_args,
    description='A simple dag ',
    schedule_interval=timedelta(1),
)


# 4.tasks

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
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

