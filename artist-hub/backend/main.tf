terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project     = google_project.commission.project_id
  credentials = file(var.credentials_file)
  region      = var.region
}

variable "project_id" {
  description = "GCP project ID for the commission website."
  type        = string
}

variable "billing_account" {
  description = "Billing account ID used to create the GCP project."
  type        = string
}

variable "org_id" {
  description = "Organization ID used to create the GCP project."
  type        = string
}

variable "credentials_file" {
  description = "Path to the Google service account JSON credentials file."
  type        = string
  default     = "./service-account.json"
}

variable "region" {
  description = "GCP region for resources."
  type        = string
  default     = "us-central1"
}

variable "firestore_location" {
  description = "Firestore location ID for native mode."
  type        = string
  default     = "us-central"
}

variable "storage_location" {
  description = "Cloud Storage bucket location."
  type        = string
  default     = "US"
}

resource "google_project" "commission" {
  name                 = "Commission Website"
  project_id           = var.project_id
  org_id               = var.org_id
  billing_account      = var.billing_account
  auto_create_network  = true
}

resource "google_firebase_project" "commission" {
  project = google_project.commission.project_id
}

resource "google_firestore_database" "commission" {
  project     = google_project.commission.project_id
  name        = "(default)"
  location_id = var.firestore_location
  type        = "NATIVE"
}

resource "google_storage_bucket" "artfiles" {
  name                        = "${var.project_id}-art-storage"
  location                    = var.storage_location
  force_destroy               = true
  uniform_bucket_level_access = true
}

output "project_id" {
  value = google_project.commission.project_id
}

output "storage_bucket" {
  value = google_storage_bucket.artfiles.name
}
