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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>
<!-- </details> -->

---

<!-- ABOUT THE PROJECT -->

## About The Project

This project is created to showcase how we can leverage `Cloud Composer` to extract the System Activities from a hosted Looker instance, into their `BigQuery` for audit and analytics purposes. For this case study, we will be exporting the *Content Usage* explore.

The following are some of the requirements:

- Extract *Content Usage* System Activities for both Initial Load and Incremental Load
- Ingest the data into `Bigquery`

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- Setup -->

## Setup

Base on the requirements, the following components are required to be setup:

- `Looker` - The Looker instance with Elite System Activities enabled
- `Looker API` - Means to extract the data from the respective System Activities explores
- `Cloud Storage` - Temporarily house the data to be sent to `Bigquery`
- `BigQuery` - Warehouse storage to save the data from the `Looker API` for audit and analytics purposes
- `IAM` - Provide the sufficient permissions to the `Cloud Composer` service account to access `Cloud Storage` and `BigQuery`
- `Cloud Composer` - Orchestrate the data flow from the `Looker API` to `BigQuery`

<p align="right">(<a href="#top">back to top</a>)</p>

### Looker 

<p align="right">(<a href="#top">back to top</a>)</p>

### Looker API 

<p align="right">(<a href="#top">back to top</a>)</p>

### Cloud Storage

<p align="right">(<a href="#top">back to top</a>)</p>

### BigQuery

<p align="right">(<a href="#top">back to top</a>)</p>

### IAM

<p align="right">(<a href="#top">back to top</a>)</p>

### Cloud Composer

<p align="right">(<a href="#top">back to top</a>)</p>

---

## Implementation

Base on the requirements, the following are the tasks in the pipelines:

- `Get Content Usage Activity` - Call the `Looker API` to retrieve the *Content Usage* data and save it to local directory (*/tmp*)
- `Disable Initial Load Flag` - Reset the initial load flag (*content_usage_initial_load*) so that the next run will be an incremental run
- `Upload Result to GCS` - Send the *Content Usage* data from local directory (*/tmp*) to the temporary `Cloud Storage`
- `Upload GCS to BigQuery` - Upload *Content Usage* data from temporary `Cloud Storage` into `BigQuery`

<p align="right">(<a href="#top">back to top</a>)</p>

### Get Content Usage Activity

<p align="right">(<a href="#top">back to top</a>)</p>

### Disable Initial Load Flag

<p align="right">(<a href="#top">back to top</a>)</p>

### Upload Result to GCS

<p align="right">(<a href="#top">back to top</a>)</p>

### Upload GCS to BigQuery

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- USAGE EXAMPLES -->

## Usage

There are 2 modes to test out the implementation
- Running Locally by executing the *api_client/looker_api_client.py*
- Running in `Cloud Composer` by uploading the *trigger-look-content-usage-dag.py* and its supporting python scripts

<p align="right">(<a href="#top">back to top</a>)</p>

### Via Local Run
The following are the execution steps to run the code locally:

- Download Packages in the *requirements.txt* for the program <br/>
    ```bash
    pip install -r requirements.txt
    ```
- Create a file from *looker.ini.example* and name it *looker.ini*. <br/>
Configure the Looker instance and API Client tokens information <br/>
NOTE: Change the looker instance port accordingly if a custom port is used
    ```
    base_url = https://<looker-instance>:19999
    client_id = <looker-api-client-id>
    client_secret = <looker-api-client-secret>
    ```

- Execute the main python script *api_client/looker_api_client.py* <br/>
NOTE: This has to be called within the *api_client* folder
    ```bash
    cd api_client
    python3 looker_api_client.py
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

### Via Cloud Composer
The following are the execution steps to run the code in `Cloud Composer`:

- Upload dag file *trigger-look-content-usage-dag.py* and its supporting python scripts into the `Cloud Composer` dag bucket
- Wait for the new version of *trigger-look-content-usage-activity* to appear in the `Cloud Composer` dag list
- Click the *trigger-look-content-usage-activity* to enter the dag details
- Click the play button to execute *trigger-look-content-usage-activity* and wait for it to be completed


<p align="right">(<a href="#top">back to top</a>)</p>

---

## Challenges

The following are some challenges encountered:

- Extracting the information via the `Looker API`

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- ROADMAP>
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p -->

<!-- CONTACT>
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p -->

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Readme Template][template-resource]

<p align="right">(<a href="#top">back to top</a>)</p>

---

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[template-resource]: https://github.com/othneildrew/Best-README-Template/blob/master/README.md

<!-- [cloud-storage-buckets]: ./images/log_analytics_pipeline.png -->
