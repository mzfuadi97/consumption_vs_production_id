# Consumption vs Production of Indonesian fisheries in 2019-2022

## Scope

This project aims to develop a path to extract, transform and load data to facilitate the creation of interactive dashboards. The aim is to visualize fisheries consumption/production trends in Indonesia and analyze these trends over time, as well as imports and exports of fisheries in Indonesia.

Additionally, this project was also part of the [DataTalksClub's Engineering Zoomcamp Certification](https://github.com/DataTalksClub/data-engineering-zoomcamp).

## Data source 

This project uses data provided by the Ministry of Fisheries and Maritime Affairs on the [official open data portal] (https://statistik.kkp.go.id/home.php), including the data that will be the material for this project.

The data set contains 10 thousand rows and 10 columns with data range from 2019 to 2022. Each row is information about each type of fish and the column contains information about production volume, consumption per province, etc.

## Dashboard

The full dashboard built in Looker Studio can be accessed [here](https://lookerstudio.google.com/s/sE1nqEbjUsk).

Please note that because the GCP free plan has 10 days of temporary access remaining, Looker Studio's connection may be lost during access. Below is the dashboard page:

![Page 1](/assets/dashboard-looker.png)

## Project Breakdown

![Architecture](/assets/Architecture.png)

The project uses the following technologies:
  * Cloud Provider - Google Cloud Platform
  * Infrastructure as Code software - Terraform
  * Containerization - Docker
  * Workflow Orchestration - Mage
  * Data Transformation - dbt
  * Data Lake - Google Cloud Storage
  * Data Warehouse - BigQuery
  * Data Visualization - Looker Studio

The Google Cloud Platform (GCP) resources are provisioned using Terraform, which sets up a Google Cloud Storage bucket for a data lake and a BigQuery dataset for a data warehouse.

Two pipelines were created using Python and SQL and they were orchestrated by Mage, which runs through a Docker container.

1) The first one is called `aki_to_gcp` and it extracts data from the Washington open data portal API, which is stored as .json, and loads it into a Google Cloud Storage bucket as partitioned .parquet files.

![pipeline 1](/assets/aki_to_gcs.png)

2) The second pipeline is called `gcs_to_bq` and it reads data from the bucket and loads it into Bigquery as a partitioned external table. 

![pipeline 2](/assets/gcs_to_bq.png)

dbt is then used, pulling the source data stored in Bigquery to perform data transformations, such as casting data types and creating fact and dimension tables with SQL.

![pipeline 2](/assets/lineage.png)

Finally, Looker Studio imports the fact table created directly from Bigquery, and then the dashboard is created. 

## How to reproduce

### Pre-requisites
* Docker
* Terraform
* Optional: A GCP Virtual Machine setup with google cloud SDK

### Steps to reproduce
1) Setup a GCP account if you don't have one. A free account can be created and it has a 90 days trial. 
2) Create a new project and take note of its ID
3) Setup a GCP service account with the following roles:  Bigquery Admin, Storage Admin, Object Storage Admin. (note: this roles give broad permission and were listed here for simplicity)
4) Create an access key for this service account and save it as `keys.json`
5) Clone this repository
6) Create a folder called 'credentials'. Save `keys.json` in this folder. 
7) CD to the 01-terraform directory. 
8) Either set up the path to credentials in `main.tf` and `variables.tf` or use
``` 
export GOOGLE_APPLICATION_CREDENTIALS=credentials/keys.json
```
9) Edit `variables.tf` with your project ID and name the bucket and dataset. 
10) Run `terraform init` and then `terraform plan`
11) Run `terraform apply` and the GCP resources will be provisioned.
12) CD to the 02-mage directory
13) Rename `dev.env` to `.env`
14) Run `docker-compose build`. Docker will pull the contents of  /02-mage and ../credentials to the container, which means `keys.json` will be accessible there.
15) Run `docker-compose up` to initialize the container. 
16) Ensure the port 6789 described in `docker-compose.yml` is fowarded
17) Edit the code blocks to include the path to your credentials and with your GCP resources. The files you should edit are in the folders `data_loaders` and `data_exporters` :
    1)  `load_aki_data.py`
    2) `ekspor_impor_ikan.py`
    3)  `load_aki_gcs.py`
    4)  `aki_to_bq.py`
18) Ensure the file `io_config.yaml` is pulling `keys.json`:
      ```
    # Google
    GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/credentials/keys.json"
    GOOGLE_LOCATION: us-west1
19) Create a [dbt](https://www.getdbt.com/) free developer account
20) Create a new project and connect it to bigquery. Provide the `keys.json` file when asked for credentials. It's possible to load the content of a repository for simplicity. You can also replicate the contents of 03-dbt. 
21) Run `dbt build`. A green confirmation message will appear if it worked properly. 
22) Check if you are able to see the fact table created in your bigquery dataset. 
23) Connect this dataset to Looker Studio and build the dashboard.

## Improvements
A possible improvement would be to automatically import the GCP resources information to the container without the need to adjust the pipeline files manually using Terraform outputs. 

## Linkedin

Please reach out to me on [Linkedin](https://www.linkedin.com/in/mzfuadi97/) if you found this project interesting and want to discuss!

Thank u [Linkedin](https://www.linkedin.com/in/bernardo-m-costa/), helped me, for example simple project  architecture with mage.ai.