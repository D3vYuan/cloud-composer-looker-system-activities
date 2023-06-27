<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h2 align="center">Looker System Activities Data Pipeline</h2>
  <p align="center">
    Case Study - Content Usage Explore
  </p>
  <!--div>
    <img src="images/profile_pic.png" alt="Logo" width="80" height="80">
  </div-->
</div>

---

<!-- TABLE OF CONTENTS -->

## Table of Contents

<!-- <details> -->
<ol>
    <li>
        <a href="#about-the-project">About The Project</a>
    </li>
    <li>
        <a href="#data">Data</a>
        <ul>
            <li><a href="#looker-to-lookml">Looker-to-LookML</a></li>
            <li><a href="#lookml-to-bigquery">LookML-to-BigQuery</a></li>
        </ul>
    </li>
    <li>
        <a href="#setup">Setup</a>
        <ul>
            <li><a href="#looker">Looker</a></li>
            <li><a href="#looker-api">Looker API</a></li>
            <li><a href="#cloud-storage">Cloud Storage</a></li>
            <li><a href="#bigquery">BigQuery</a></li>
            <li><a href="#iam">IAM</a></li>
            <li><a href="#cloud-composer">Cloud Composer</a></li>
        </ul>
    </li>
    <li>
        <a href="#implementation">Implementation</a>
        <ul>
            <li><a href="#get-content-usage-activity">Get Content Usage Activity </a></li>
            <li><a href="#disable-initial-load-flag">Disable Initial Load Flag</a></li>
            <li><a href="#upload-result-to-gcs">Upload Result to GCS</a></li>
            <li><a href="#upload-gcs-to-bigquery">Upload GCS to BigQuery</a></li>
        </ul>
    </li>
    <li><a href="#usage">Usage</a>
        <ul>
            <li><a href="#via-local-run">Via Local Run</a></li>
            <li><a href="#via-cloud-composer">Via Cloud Composer</a></li>
        </ul>
    </li>
    <li><a href="#challenges">Challenges</a></li>
    <li><a href="#possible-enhancements">Possible Enhancements</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>
<!-- </details> -->

---

<!-- ABOUT THE PROJECT -->

## About The Project

This project is created to showcase how we can leverage `Cloud Composer` to extract the System Activities from a hosted Looker instance, into `BigQuery` for audit and analytics purposes. <br/>
For this case study, we will be exporting the *Content Usage* explore.

The following are some of the requirements:

- Extract *Content Usage* System Activities for both Initial Load and Incremental Load
- Ingest the data into `Bigquery`

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- Data -->

## Data

Base on the requirements, the following data mapping are required:
- `Looker to LookML` - Map the fields from the explore to their underlying fields to extract the data via `Looker API`
- `LookML to BigQuery` - Map the looker fields into bigquery fields to ingest the data into `BigQuery`

<p align="right">(<a href="#top">back to top</a>)</p>

### Looker to LookML

This task will map the fields from the explore to their underlying fields to extract the data via `Looker API` <br/>
The *LookML* field can be extracted by clicking the *information* icon beside the *Explore* field.

| ![looker-lookml-fields-extract][looker-lookml-fields-extract] | 
|:--:| 
| *Looker to LookML Field Mapping* |

<br/>

The following are the mappings for *Content Usage* explore:

|#|Dimensions|LookML|
|--|--|--|
|1|Content ID|content_usage.content_id|
|2|Content Title|content_usage.content_title|
|3|Content Type|content_usage.content_type|
|4|Days Since Last Access Tiers|content_usage.days_since_last_access_tiers|
|5|Days Since Last Accessed|content_usage.days_since_last_accessed|
|6|ID|content_usage.id|
|7|Incremented Counts > API Count|content_usage.api_count|
|8|Incremented Counts > Embed Count|content_usage.embed_count|
|9|Incremented Counts > Favourite Count|content_usage.favorite_count|
|10|Incremented Counts > Public Count|content_usage.public_count|
|11|Incremented Counts > Schedule Count|content_usage.schedule_count|
|12|Incremented Counts > View Count|content_usage.other_count|
|13|Last Accessed Date > Time|content_usage.last_accessed_time|

<br/>

`NOTE:` Only *content_usage.last_accessed_time* is extracted as the rest of the *last_accessed_* fields are just drill down or slices of this field

<p align="right">(<a href="#top">back to top</a>)</p>

### LookML to BigQuery

This task will map the fields from the looker to their corresponding fields in `BigQuery` <br/>

<br/>

The following are the mappings for *Content Usage* explore:

|#|LookML|BigQuery|
|--|--|--|
|1|content_usage.content_id|content_id|
|2|content_usage.content_title|content_title|
|3|content_usage.content_type|content_type|
|4|content_usage.days_since_last_access_tiers|days_since_last_access_tiers|
|5|content_usage.days_since_last_accessed|days_since_last_accessed|
|6|content_usage.id|id|
|7|content_usage.api_count|api_count|
|8|content_usage.embed_count|embed_count|
|9|content_usage.favorite_count|favorite_count|
|10|content_usage.public_count|public_count|
|11|content_usage.schedule_count|schedule_count|
|12|content_usage.other_count|other_count|
|13|content_usage.last_accessed_time|last_accessed_time|

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- Setup -->

## Setup
<div id="cloud-composer-setup"></div>

Base on the requirements, the following components are required to be setup:

- `Looker API` - Means to extract the data from the respective System Activities explores
- `Looker` - The Looker instance with Elite System Activities enabled
- `Cloud Storage` - Temporarily house the data to be sent to `Bigquery`
- `BigQuery` - Warehouse storage to save the data from the `Looker API` for audit and analytics purposes
- `IAM` - Provide the sufficient permissions to the `Cloud Composer` service account to access `Cloud Storage` and `BigQuery`
- `Cloud Composer` - Orchestrate the data flow from the `Looker API` to `BigQuery`

<p align="right">(<a href="#top">back to top</a>)</p>

### Looker API 
The method *run_inline_query* will be used to extract the data from the *Content Usage* explore <br/>

The following is a sample body for the *run_inline_query*: <br/>
`NOTE:` Minimally, the request body should contains *model*, *view*, and *fields*
```json
{
  "model": "system__activity",
  "view": "content_usage",
  "fields": ["content_usage.content_id", "content_usage.content_title", "content_usage.content_type"]
}
```

| ![looker-api-explorer-request][looker-api-explorer-request] | 
|:--:| 
| *run_inline_query request* |

<br/>

| ![looker-api-explorer-response][looker-api-explorer-response] | 
|:--:| 
| *run_inline_query response* |

<p align="right">(<a href="#top">back to top</a>)</p>

### Looker 
<div id="looker-api-account"></div>

Generate access token for the user accessing `Looker API`. Under Admin > Locate the User Account to use for the `Looker API` > Click to see details of User Account > Under API Keys, click Edit Keys > Create New Keys <br/>

`NOTE:` You will need to assign the User Account with sufficient privileges to view the System Activities in `Looker` <br/>

| ![looker-api-user-account][looker-api-user-account] | 
|:--:| 
| *Looker API User Account* |

<br/>

| ![looker-api-user-keys][looker-api-user-keys] | 
|:--:| 
| *Looker API User Key* |

<p align="right">(<a href="#top">back to top</a>)</p>

### Cloud Storage

#### Jsonlines Files
<div id="looker-bucket-creation"></div>

Create the bucket to house the temporary output file from the `Looker API` <br/>

| ![cloud-storage-temporary-bucket][cloud-storage-temporary-bucket] | 
|:--:| 
| *Temporary Bucket to hold the Looker API data* |

Set the Lifecycle Management for the bucket to housekeep jsonlines (*jsonl*) files to optimize for storage and costing. In the following, all jsonlines(*jsonl*) files more than 3 days will be delete from the bucket <br/>

| ![cloud-storage-lifecycle][cloud-storage-lifecycle] | 
|:--:| 
| *Looker API User Key* |

<p align="right">(<a href="#top">back to top</a>)</p>

#### Dag Files
The following are the files to be uploaded to the `Cloud Composer` dag directory: <br/>

| ![cloud-composer-hosted-dag-folder][cloud-composer-hosted-dag-folder] | 
|:--:| 
| *Cloud Composer Dag Folder* |

<br/>

| ![cloud-storage-dag-python][cloud-storage-dag-python] | 
|:--:| 
| *Cloud Composer Dag Files* |

<br/>

<p align="right">(<a href="#top">back to top</a>)</p>

### BigQuery
<div id="bigquery-creation"></div>

Create the table (*Content_Usage*) to house the *Content Usage* data with the following fields:

<br/>

|#|Name|Type|Mode
|--|--|--|--|
|1|content_id|String|Nullable|
|2|content_title|String|Nullable|
|3|content_type|String|Nullable|
|4|days_since_last_access_tiers|String|Nullable|
|5|days_since_last_accessed|Integer|Nullable|
|6|id|Integer|Nullable|
|7|api_count|Integer|Nullable|
|8|embed_count|Integer|Nullable|
|9|favorite_count|Integer|Nullable|
|10|public_count|Integer|Nullable|
|11|schedule_count|Integer|Nullable|
|12|other_count|Integer|Nullable|
|13|last_accessed_time|Datetime|Nullable|

<br/>

| ![bigquery-fields-schema][bigquery-fields-schema] | 
|:--:| 
| *BigQuery Content_Usage Schema* |

<p align="right">(<a href="#top">back to top</a>)</p>

### IAM

Assign the sufficient permissions for the `Cloud Composer` service account to access `Cloud Storage` and `BigQuery` during the dag run.

| ![cloud-composer-hosted-sa][cloud-composer-hosted-sa] | 
|:--:| 
| *Cloud Composer Service Account* |

<br>

`NOTE:` While the following image shows the service account being assigned *admin* rights, one may just provide sufficient permissions to the account for accessing `Cloud Storage` and `BigQuery` <br/>

| ![cloud-composer-hosted-sa-permissions][cloud-composer-hosted-sa-permissions] | 
|:--:| 
| *Cloud Composer Service Account Privileges* |

<p align="right">(<a href="#top">back to top</a>)</p>

### Cloud Composer

#### Install Dependencies

The following are the dependencies needed for the dag run:

|#|Dependencies|Description
|--|--|--|
|1|json-converter|Use to map the json into another format|
|2|jsonlines|Use to map the json into json lines to be ingested into Bigquery|
|3|looker-sdk|Use to call the Looker API|

<br/>

| ![cloud-composer-hosted-dependencies][cloud-composer-hosted-dependencies] | 
|:--:| 
| *Cloud Composer Dependencies* |

<p align="right">(<a href="#top">back to top</a>)</p>

#### Setup Variables

The following are the variables needed for the dag run:

|#|Variables|Description|Example
|--|--|--|--|
|1|bigquery_content_usage_schema|The schema for the content_usage table. <br/> (*jsonline value*)|{'name': 'content_id', 'type': 'STRING', 'mode': 'NULLABLE'},<br/>{'name': 'content_title', 'type': 'STRING', 'mode': 'NULLABLE'},<br/>{'name': 'content_type', 'type': 'STRING', 'mode': 'NULLABLE'},<br/>{'name': 'days_since_last_access_tiers', 'type': 'STRING', 'mode': 'NULLABLE'},<br/>{'name': 'days_since_last_accessed', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'id', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'api_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'embed_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'favorite_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'public_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'schedule_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'other_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},<br/>{'name': 'last_accessed_time', 'type': 'DATETIME', 'mode': 'NULLABLE'}
|2|bigquery_content_usage_table|The table in bigquery to save the content usage activities|content_usage|
|3|bigquery_dataset_id|The dataset id of the bigquery for saving the looker system activities|<p>Please refer to <a href="#bigquery-creation">bigquery creation</a></p>|
|4|bigquery_location|The location of the bigquery|us-central1|
|5|bigquery_project_id|The project id for bigquery|<p>Please refer to <a href="#bigquery-creation">bigquery creation</a></p>|
|6|content_usage_fields|The fields to be extracted from content usage. <br/> (*comma separated value*)|content_usage.content_id, content_usage.content_title, content_usage.content_type, content_usage.days_since_last_access_tiers,content_usage.days_since_last_accessed, content_usage.id,content_usage.api_count,content_usage.embed_count,content_usage.favorite_count, content_usage.public_count,content_usage.schedule_count,content_usage.other_count, content_usage.last_accessed_time|
|7|content_usage_filters|The filters to be extracted from content usage. Applicable only if *content_usage_initial_load* is set to false. <br/> (*json value*)|{ "content_usage.last_accessed_time": "1 day ago" }|
|8|content_usage_initial_load|Indicates if content_usage table is initial load|false|
|9|looker_api_base_url|The url to access the looker api|https://\<looker-instance-name\>:19999|
|10|looker_api_bucket_name|GCS Bucket Name to store the system activity result|<p>Please refer to <a href="#looker-bucket-creation">looker bucket creation</a></p>|
|11|looker_api_client_id|The client id for calling the Looker API|<p>Please refer to <a href="#looker-api-account">looker api account</a></p>|
|12|looker_api_client_secret|The client secret for calling the Looker API|<p>Please refer to <a href="#looker-api-account">looker api account</a></p>|
|13|looker_api_timeout|The timeout in seconds for the api calls|120|
|14|looker_api_verify_ssl|Whether to verify ssl for the looker api|false|

<br/>

| ![cloud-composer-hosted-variables][cloud-composer-hosted-variables] | 
|:--:| 
| *Cloud Composer Variables* |

<p align="right">(<a href="#top">back to top</a>)</p>

---

## Implementation

<br/>

| ![cloud-composer-pipeline][cloud-composer-pipeline] | 
|:--:| 
| *Cloud Composer Data Pipeline* |

<br/>

Base on the requirements, the following are the tasks in the pipelines:

- `Get Content Usage Activity` - Call the `Looker API` to retrieve the *Content Usage* data and save it to local directory (*/tmp*)
- `Disable Initial Load Flag` - Reset the initial load flag (*content_usage_initial_load*) so that the next run will be an incremental run
- `Upload Result to GCS` - Send the *Content Usage* data from local directory (*/tmp*) to the temporary `Cloud Storage`
- `Upload GCS to BigQuery` - Upload *Content Usage* data from temporary `Cloud Storage` into `BigQuery`

<p align="right">(<a href="#top">back to top</a>)</p>

### Get Content Usage Activity
This task make use of the `Looker API` to retrieve the *Content Usage* data and save it to local directory (*/tmp*). <br/>
It will then return the **source file** (*content_usage_source_file*) and **destination file** (*content_usage_dest_file*) which can be used by other downstream tasks.
<br/>

```python
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
```
<p align="right">(<a href="#top">back to top</a>)</p>

### Disable Initial Load Flag
This task will reset the **initial load flag** (*content_usage_initial_load*) so that the next run will be an incremental run. 
<br/>

```python
@task(task_id="disable_initial_load_flag")
    def disable_initial_load():
        # Disable initial load after the first load
        if CONTENT_USAGE_INITIAL_LOAD:
            Variable.set(key = "content_usage_initial_load", 
                         value = "false",
                         description = "Indicates if content_usage table is initial load")
```
<p align="right">(<a href="#top">back to top</a>)</p>

### Upload Result to GCS
This task will send the *Content Usage* data from local directory (*/tmp*) to the temporary `Cloud Storage`. <br/>
It make use of the result from the *Get Content Usage Activity* to locate the source and destination file
<br/>

```python
upload_file_task = LocalFilesystemToGCSOperator(
        task_id="upload_result_to_gcs",
        src="{{task_instance.xcom_pull('get_content_usage_activity')['content_usage_source_file']}}",
        dst="{{task_instance.xcom_pull('get_content_usage_activity')['content_usage_dest_file']}}",
        bucket=BUCKET_NAME,
    )
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Upload GCS to BigQuery
This task will upload *Content Usage* data from temporary `Cloud Storage` into `BigQuery`. <br/>
The format of the file should be in **jsonlines** (*jsonl*) format and it will just append to the specify table. <br/>
`NOTE:` The appending of data might leads to duplication in the `BigQuery` table
<br/>

```python
gcs_to_bq_task = GCSToBigQueryOperator(
        task_id='upload_gcs_to_bigquery',
        bucket=BUCKET_NAME,
        source_objects=["{{task_instance.xcom_pull('get_content_usage_activity')['content_usage_dest_file']}}"],
        destination_project_dataset_table=f"{BIGQUERY_DATASET_ID}.{BIGQUERY_TABLE_NAME}",
        schema_fields=BIGQUERY_TABLE_SCHEMA,
        write_disposition='WRITE_APPEND',
        source_format = "NEWLINE_DELIMITED_JSON",
    );
```


<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- USAGE EXAMPLES -->

## Usage

There are 2 modes to test out the implementation
- Running Locally by executing the *api_client/looker_api_client.py*
- Running in `Cloud Composer` by uploading the *trigger-look-content-usage-dag.py* and its supporting python scripts

<p align="right">(<a href="#top">back to top</a>)</p>

### Via Local Run
`NOTE:` This mode of run only generate the jsonline (*jsonl*) file for the *Content Usage*. One has to then manually import this file into `BigQuery` to see the result.

The following are the execution steps to run the code locally:

- Download Packages in the *requirements.txt* for the program <br/>
    ```bash
    pip install -r requirements.txt
    ```
- Create a file from *looker.ini.example* and name it *looker.ini*. <br/>
Configure the Looker instance and API Client tokens information <br/>
`NOTE:` Change the looker instance port accordingly if a custom port is used
    ```
    base_url = https://<looker-instance>:19999
    client_id = <looker-api-client-id>
    client_secret = <looker-api-client-secret>
    ```

- Execute the main python script *api_client/looker_api_client.py* <br/>
`NOTE:` This has to be called within the *api_client* folder
    ```bash
    cd api_client
    python3 looker_api_client.py
    ```

- Verify that the program executed successfully and generated the output file <br/>
    **Logs** <br/>

    | ![cloud-composer-local-log][cloud-composer-local-log] | 
    |:--:| 
    | *Cloud Composer Local Run Log* |

    <br/>

    **Output** <br/>

    | ![cloud-composer-local-output][cloud-composer-local-output] | 
    |:--:| 
    | *Cloud Composer Local Run Output* |

<p align="right">(<a href="#top">back to top</a>)</p>

### Via Cloud Composer
`NOTE:` Assuming that the `Cloud Composer` setup steps have been completed, otherwise see <a href="#cloud-composer-setup">here</a> before proceeding. <br/>

The following are the execution steps to run the code in `Cloud Composer`:

- Upload dag file *trigger-look-content-usage-dag.py* and its supporting python scripts into the `Cloud Composer` dag bucket <br/>
    **Dag Files** <br/>

    | ![cloud-composer-hosted-dag-files][cloud-composer-hosted-dag-files] | 
    |:--:| 
    | *Cloud Composer Dag Files* |

- Wait for the new version of *trigger-look-content-usage-activity* to appear in the `Cloud Composer` dag list
- Click the *trigger-look-content-usage-activity* to enter the dag details <br/>
    **Dag** <br/>

    | ![cloud-composer-hosted-dag][cloud-composer-hosted-dag] | 
    |:--:| 
    | *Cloud Composer Dag* |

- Click the play button to execute *trigger-look-content-usage-activity* and wait for it to be completed <br/>
    **Dag** <br/>

    | ![cloud-composer-hosted-dag-run][cloud-composer-hosted-dag-run] | 
    |:--:| 
    | *Cloud Composer Run Dag* |

- Verify that the program executed successfully and generated the output file <br/>
    **Log** <br/>

    | ![cloud-composer-hosted-log][cloud-composer-hosted-log] | 
    |:--:| 
    | *Cloud Composer Run Log* |

    **Output** <br/>

    | ![cloud-composer-hosted-output][cloud-composer-hosted-output] | 
    |:--:| 
    | *Cloud Composer Run Output* |
    
- Verify that the program executed successfully and inserted the data into `BigQuery` <br/>
    **BigQuery** <br/>

    | ![cloud-composer-hosted-bq][cloud-composer-hosted-bq] | 
    |:--:| 
    | *BigQuery Output* |

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- Challenges -->
## Challenges

The following are some challenges encountered:
- Extracting the information via the `Looker API`
<p align="right">(<a href="#top">back to top</a>)</p>

### Challenge #1: Extracting information via the `Looker API`

In order for us to process the data, we need to know the type of format that `Looker API` return for us to perform any transformation on it. 
Lucky for us, there is `API Explorer` that are available in the `Looker` marketplace.

| ![looker-api-explorer-application][looker-api-explorer-application] | 
|:--:| 
| *Looker API Explorer* |

<br/>

Once installed, it will appear in the application sidebar and we can launch it to try out the various endpoints which `Looker API` offers. <br/>
`NOTE:` You might need to disable *developer mode* for the `API Explorer` to work

| ![looker-api-explorer-request][looker-api-explorer-request] | 
|:--:| 
| *Looker API Request* |

<br/>

| ![looker-api-explorer-response][looker-api-explorer-response] | 
|:--:| 
| *Looker API Response* |

<br/>

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- Enhancements -->
## Possible Enhancements

- [ ] Add Masking of Sensitive Data before ingesting to `BigQuery`
- [ ] Add Deduplication Step for Data before Ingesting to `BigQuery`
- [ ] Add Exception handling if previous day has no data (Currently, it will show as `fail` in pipeline)
- [ ] Add Support for the Rest of the System Activities
- [ ] Add Support for multiple Looker instance

<!-- See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues). -->

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT>
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p -->

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [System Activities Explores][ref-esa-explores]
- [System Activities Dashboards][ref-esa-dashboards]
- [Solution to export Elite System Activites Log][ref-support-export-esa]
- [Parameters to Looker API][ref-looker-api-parameters]
- [Readme Template][template-resource]

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[template-resource]: https://github.com/othneildrew/Best-README-Template/blob/master/README.md
[ref-esa-explores]: https://cloud.google.com/looker/docs/usage-reports-with-system-activity-explores
[ref-esa-dashboards]: https://cloud.google.com/looker/docs/system-activity-dashboards
[ref-support-export-esa]: https://www.googlecloudcommunity.com/gc/Developing-Applications/Write-the-result-of-a-Looker-query-to-BigQuery-with-Cloud/m-p/576853
[ref-looker-api-parameters]: https://www.googlecloudcommunity.com/gc/Developing-Applications/Can-I-query-system-activity-explores-using-sdk-method/m-p/576926

[looker-lookml-fields-extract]: ./image/looker-to-lookml-fields-extraction.png
[bigquery-fields-schema]: ./image/bigquery-fields-schema.png

[looker-api-explorer-application]: ./image/looker-api-explorer-application.png
[looker-api-explorer-request]: ./image/looker-api-explorer-request.png
[looker-api-explorer-response]: ./image/looker-api-explorer-response.png

[looker-api-user-account]: ./image/looker-api-user-account.png
[looker-api-user-keys]: ./image/looker-api-user-keys.png

[cloud-storage-temporary-bucket]: ./image/cloud-storage-temporary-bucket.png
[cloud-storage-lifecycle]: ./image/cloud-storage-lifecycle-management.png
[cloud-storage-dag-python]: ./image/cloud-storage-dag-python.png

[cloud-storage-temporary-bucket]: ./image/looker-api-temporary-bucket.png

[cloud-composer-pipeline]: ./image/cloud-composer-pipeline.png
[cloud-composer-local-log]: ./image/cloud-composer-local-log.png
[cloud-composer-local-output]: ./image/cloud-composer-local-output.png

[cloud-composer-hosted-sa]: ./image/cloud-composer-hosted-service-account.png
[cloud-composer-hosted-sa-permissions]: ./image/cloud-composer-hosted-service-account-permissions.png

[cloud-composer-hosted-dependencies]: ./image/cloud-composer-hosted-dependencies.png
[cloud-composer-hosted-variables]: ./image/cloud-composer-hosted-variables.png
[cloud-composer-hosted-dag-folder]: ./image/cloud-composer-hosted-dag-folder.png
[cloud-composer-hosted-dag-files]: ./image/cloud-composer-hosted-dag-files.png
[cloud-composer-hosted-dag-run]: ./image/cloud-composer-hosted-dag-run.png
[cloud-composer-hosted-dag]: ./image/cloud-composer-hosted-dag.png
[cloud-composer-hosted-log]: ./image/cloud-composer-hosted-log.png
[cloud-composer-hosted-output]: ./image/cloud-composer-hosted-output.png
[cloud-composer-hosted-bq]: ./image/cloud-composer-hosted-bq.png
<!-- [cloud-storage-buckets]: ./images/log_analytics_pipeline.png -->
