
from datetime import datetime, timedelta
from textwrap import dedent

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator


default_args={
    'depends_on_past': False,
    'owner': 'airflow',
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
    }
 
dag = DAG(
    'ETL',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args=default_args,
    description='ETL Tasks',
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
    catchup=False,
    tags=['ETL'],
)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='get_file',
    bash_command='wget -O /workspace/src/staging/tolldata.tgz https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz ',
    dag = dag
)

t2 = BashOperator(
    task_id='unzip_data',
    bash_command='tar -C /workspace/src/staging/files -xzf /workspace/src/staging/tolldata.tgz',
    dag = dag
)

t3 = BashOperator(
    task_id = 'extract_data_from_csv',
    bash_command= 'cut -d\',\' -f1,2,3,4 /workspace/src/staging/files/vehicle-data.csv >  /workspace/src/staging/extracted_data/csv_data.csv',
    dag = dag
)

t4 = BashOperator(
    task_id = 'extract_data_from_tsv',
    bash_command= '''awk -F'\t' 'BEGIN {OFS=","} {gsub("\\r", "", $NF); print $5,$6,$NF}' /workspace/src/staging/files/tollplaza-data.tsv >  /workspace/src/staging/extracted_data/tsv_data.csv''',
    dag = dag
)

t5 = BashOperator(
    task_id = 'extract_data_from_fixed_width',
    bash_command= "awk '{print substr($0,length($0)-8,9)}' /workspace/src/staging/files/payment-data.txt | tr ' ' ',' >  /workspace/src/staging/extracted_data/fixed_width_data.csv",
    dag = dag
)

t6 = BashOperator(
    task_id = 'consolidate_data',
    bash_command= "cd /workspace/src/staging/extracted_data; paste -d ',' csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv",
    dag = dag
)

t7 = BashOperator(
    task_id = 'transform_data',
    bash_command = '''awk -F',' 'BEGIN {OFS=","} NF > 1{$4 = toupper($4)} 1' /workspace/src/staging/extracted_data/extracted_data.csv > /workspace/src/staging/transformed_data/transformed_data.csv''',
    dag = dag
)

t1 >> t2
t2 >> [t3,t4,t5]
[t3,t4,t5] >> t6
t6 >> t7
