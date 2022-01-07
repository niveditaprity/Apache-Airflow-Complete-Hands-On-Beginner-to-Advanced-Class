from datetime import datetime, timedelta
from pathlib import Path
from airflow import DAG
import pandas as pd
from airflow.operators.python_operator import PythonOperator

from airflow.utils.dates import days_ago


import os
import sqlite3
from pandas.io.sql import SQLiteDatabase, SQLiteTable
# get dag directory path
dag_path=os.getcwd()


# default arguments
default_args={
    'owner':'nivedita',
    'start_date':days_ago(5)
}
# dag instantiate
ingestion_dag=DAG(
    'booking_ingestion',
    default_args=default_args,
    description='aggregates  booking records for data analysis',
    schedule_interval=timedelta(days=1),
    catchup=False
)

def transform_data(exec_date):
    try:
        print(f"Ingesting data for date: {exec_date}")
        date = datetime.strptime(exec_date, '%Y-%m-%d %H')
        file_date_path = f"{date.strftime('%Y-%m-%d')}/{date.hour}"

        booking = pd.read_csv(f"{dag_path}/data/booking.csv", low_memory=False)
        client = pd.read_csv(f"{dag_path}/data/client.csv", low_memory=False)
        hotel = pd.read_csv(f"{dag_path}/data/hotel.csv", low_memory=False)

        # merge booking with client
        data = pd.merge(booking, client, on='client_id')
        data.rename(columns={'name': 'client_name', 'type': 'client_type'}, inplace=True)

        # merge booking, client & hotel
        data = pd.merge(data, hotel, on='hotel_id')
        data.rename(columns={'name': 'hotel_name'}, inplace=True)

        # make date format consistent
        data.booking_date = pd.to_datetime(data.booking_date, infer_datetime_format=True)

        # make all cost in GBP currency
        data.loc[data.currency == 'EUR', ['booking_cost']] = data.booking_cost * 0.8
        data.currency.replace("EUR", "GBP", inplace=True)

        # remove unnecessary columns
        data = data.drop('address', 1)

        # load processed data
        output_dir = Path(f'{dag_path}/processed_data/{file_date_path}')
        output_dir.mkdir(parents=True, exist_ok=True)
        # processed_data/2021-08-15/12/2021-08-15_12.csv
        data.to_csv(output_dir / f"{file_date_path}.csv".replace("/", "_"), index=False, mode='a')

    except ValueError as e:
        print("datetime format should match %Y-%m-%d %H", e)
        raise e


def load_data(exec_date):
    print(f"Loading data for date: {exec_date}")
    date = datetime.strptime(exec_date, '%Y-%m-%d %H')
    file_date_path = f"{date.strftime('%Y-%m-%d')}/{date.hour}"

    conn = sqlite3.connect("/Users/admin/Desktop/airflow-tutorial/airflow.db")
    c = conn.cursor()
    c.execute('''
                CREATE TABLE IF NOT EXISTS booking_record (
                    client_id INTEGER NOT NULL,
                    booking_date TEXT NOT NULL,
                    room_type TEXT(512) NOT NULL,
                    hotel_id INTEGER NOT NULL,
                    booking_cost NUMERIC,
                    currency TEXT,
                    age INTEGER,
                    client_name TEXT(512),
                    client_type TEXT(512),
                    hotel_name TEXT(512)
                );
             ''')
    processed_file = f"{dag_path}/processed_data/{file_date_path}/{file_date_path.replace('/', '_')}.csv"
    records = pd.read_csv(processed_file)
    records.to_sql('booking_record', conn, index=False, if_exists='append')



task_1 = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_args=["{{ ds }} {{ execution_date.hour }}"],
    dag=ingestion_dag,
)

task_2 = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    op_args=["{{ ds }} {{ execution_date.hour }}"],
    dag=ingestion_dag,
)


task_1 >> task_2
