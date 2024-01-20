terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.83.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# module "bitcoin-rg" {
#   source               = "./modules/aks"
#   resource_group_name  = var.resource_group_name
#   location             = var.location
# }

module "bitcoin-aks" {
  source       = "./modules/aks"
  cluster_name = var.cluster_name
  dns_prefix   = var.dns_prefix
  location     = var.location
  resource_group_name = var.resource_group_name
}
