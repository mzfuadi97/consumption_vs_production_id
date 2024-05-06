locals {
  data_lake_bucket = "perikanan_indo_bucket"
}

variable "project" {
  description = "Your GCP Project ID"
  default     = "secret-meridian-414302"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default     = "us-west1"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "perikanan_indo"
}
