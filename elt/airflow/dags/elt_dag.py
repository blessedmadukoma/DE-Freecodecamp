from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_reply': False,
}

def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"ELT script failed with error:{result.stderr}")
    else:
        print(result.stdout)

# create the DAG (Directed Acyclic Graph)
dag = DAG(
    'elt_and_dbt', # name of the DAG
    default_args=default_args,
    description="An ELT workflow with dbt",
    start_date=datetime(2024, 3, 1), # year, month, day
    catchup=False,
)

# tasks
# task 1: run the elt script
task1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_elt_script,
    dag=dag
)

# task 2: run dbt
task2 = DockerOperator(
    task_id="dbt_run",
    image="ghcr.io/dbt-labs/dbt-postgres:1.4.7",
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt",
        "--full-refresh"
      ],
      auto_remove=True,
      network_mode="bridge",
      mounts=[
        Mount(source='/Users/blessedmadukoma/Desktop/Code/learn/data-engineering/freecodecamp/elt/custom_postgres_freecodecamp', target='/opt/dbt', type='bind'),
        Mount(source='/Users/blessedmadukoma/.dbt', target='/root', type='bind'),
    ],
    dag=dag
)

# set the order of execution/operation: task1 has to run before task2
task1 >> task2