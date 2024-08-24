from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.docker_operator import DockerOperator
from etl import start_etl
from modelling import start_modelling


default_args = {
    'owner': 'kelompok 3',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='final_project_dag',
    default_args=default_args,
    description='This is our first dag that we write',
    start_date=datetime(2022, 12, 16, 5),
    schedule_interval='@daily'
) as dag:

    start_dag = DummyOperator(
        task_id="start_dag"
    )

    end_dag = DummyOperator(
        task_id="end_dag"
    )

    task1 = BashOperator(
        task_id='print_date',
        bash_command="scripts/print_date.sh"
    )

    task2 = PythonOperator(
        task_id='extract',
        python_callable=start_etl,
    )

    task3 = PythonOperator(
        task_id='modelling',
        python_callable=start_modelling,
    )

    start_dag >> task1 >> task2 >> task3 >> end_dag
