variable "cluster_name" {
  type        = string
  description = "Name of the AKS cluster"
}

variable "dns_prefix" {
  type        = string
  description = "DNS prefix for the AKS cluster"
}

variable "resource_group_name" {
  type        = string
  description = "Name of the resource group"
  
}

variable "location" {
  type        = string
  description = "Location of the resource group"
}