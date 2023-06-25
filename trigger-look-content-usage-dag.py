
from datetime import datetime as dt
from datetime import timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.utils.dates import days_ago
from airflow.models.xcom_arg import PlainXComArg
from airflow.models import Variable
from utils.variable_utils import convert_bq_schema_to_string, convert_string_to_bool, convert_string_to_list
import logging
logger = logging.getLogger(__name__)

PROJECT_ID = Variable.get("bigquery_project_id")
BUCKET_NAME = Variable.get("looker_api_bucket_name")

BIGQUERY_LOCATION = Variable.get("bigquery_location")
BIGQUERY_DATASET_ID = Variable.get("bigquery_dataset_id")
BIGQUERY_TABLE_NAME = Variable.get("bigquery_content_usage_table")

BIGQUERY_TABLE_SCHEMA_ITEMS = Variable.get("bigquery_content_usage_schema")
BIGQUERY_TABLE_SCHEMA = convert_bq_schema_to_string(BIGQUERY_TABLE_SCHEMA_ITEMS)

CONTENT_USAGE_INITIAL_LOAD = convert_string_to_bool(Variable.get("content_usage_initial_load"))
CONTENT_USAGE_FIELDS = convert_string_to_list(Variable.get("content_usage_fields"))
CONTENT_USAGE_FILTERS = Variable.get("content_usage_filters", deserialize_json=True)

# print(f"[Test] Raw: {BIGQUERY_TABLE_SCHEMA_ITEMS} - {type(BIGQUERY_TABLE_SCHEMA_ITEMS)}")
# print(f"[Test] Schema: {BIGQUERY_TABLE_SCHEMA} - {type(BIGQUERY_TABLE_SCHEMA)}")
# print(f"[Test] Initial Load: {CONTENT_USAGE_INITIAL_LOAD} - {type(CONTENT_USAGE_INITIAL_LOAD)}")
# print(f"[Test] Fields: {CONTENT_USAGE_FIELDS} - {type(CONTENT_USAGE_FIELDS)}")
# print(f"[Test] Filters: {CONTENT_USAGE_FILTERS} - {type(CONTENT_USAGE_FILTERS)}")

dag_owner = 'airflow'

default_args = {'owner': dag_owner,
        'start_date': dt.now() - timedelta(days=1),
        'depends_on_past': False,
        'retries': 0,
        'email_on_failure': False,
        'email_on_retry': False,
        'catchup': False,
        'retry_delay': timedelta(minutes=5),
        }

with DAG(dag_id='trigger-look-content-usage-activity',
        default_args=default_args,
        description='Data pipeline to extract information from the content usage table',
        schedule_interval='@daily',
        max_active_runs=1,
        tags=['bigquery', 'looker']
):
    start = EmptyOperator(task_id='start')

    @task(task_id="get_content_usage_activity")
    def get_system_activity() -> PlainXComArg:
        from api_client.looker_api_client import get_content_usage_look
        import os

        current_timestamp=dt.now().strftime("%Y%m%d")
        source_file = get_content_usage_look(execution_timestamp = current_timestamp,
                                             data_fields = CONTENT_USAGE_FIELDS,
                                             data_filters = CONTENT_USAGE_FILTERS,
                                             initial_load = CONTENT_USAGE_INITIAL_LOAD)
        destination_file = os.path.basename(source_file)

        return {
            "content_usage_source_file" : source_file,
            "content_usage_dest_file" : destination_file,
        }

    @task(task_id="disable_initial_load_flag")
    def disable_initial_load():
        # Disable initial load after the first load
        if CONTENT_USAGE_INITIAL_LOAD:
            Variable.set(key = "content_usage_initial_load", 
                         value = "false",
                         description = "Indicates if content_usage table is initial load")

    get_activity_task = get_system_activity()
    disable_initial_load_task = disable_initial_load()
    # print(f"results: {str(get_activity_task['return_value'])} - {type(get_activity_task['return_value'])}")

    upload_file_task = LocalFilesystemToGCSOperator(
        task_id="upload_result_to_gcs",
        src="{{task_instance.xcom_pull('get_content_usage_activity')['content_usage_source_file']}}",
        dst="{{task_instance.xcom_pull('get_content_usage_activity')['content_usage_dest_file']}}",
        bucket=BUCKET_NAME,
    )

    gcs_to_bq_task = GCSToBigQueryOperator(
        task_id='upload_gcs_to_bigquery',
        bucket=BUCKET_NAME,
        source_objects=["{{task_instance.xcom_pull('get_content_usage_activity')['content_usage_dest_file']}}"],
        destination_project_dataset_table=f"{BIGQUERY_DATASET_ID}.{BIGQUERY_TABLE_NAME}",
        schema_fields=BIGQUERY_TABLE_SCHEMA,
        # https://cloud.google.com/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata.WriteDisposition
        # write_disposition='WRITE_TRUNCATE'
        write_disposition='WRITE_APPEND',
        source_format = "NEWLINE_DELIMITED_JSON",
    );

    end = EmptyOperator(task_id='end')

    start >> get_activity_task >> disable_initial_load_task >> upload_file_task >> gcs_to_bq_task >> end
