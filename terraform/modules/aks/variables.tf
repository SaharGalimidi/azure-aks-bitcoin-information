# path: azure-aks-bitcoin-information\terraform\modules\aks\variables.tf
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

variable "role_based_access_control_enabled" {
  type        = bool
  description = "Enable Role Based Access Control"
  default     = true
}

variable "azure_active_directory_role_based_access_control" {
  type        = bool
  description = "Enable Azure Active Directory Role Based Access Control"
  default     = true
}


variable "role_definition_name" {
  type        = string
  description = "Role assignment"
  default = "Azure Kubernetes Service RBAC Cluster Admin"
}

variable "location" {
  type        = string
  description = "Location of the resource group"
}