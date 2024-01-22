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

module "bitcoin-aks" {
  source       = "./modules/aks"
  cluster_name = var.cluster_name
  dns_prefix   = var.dns_prefix
  location     = var.location
  resource_group_name = var.resource_group_name
}

resource "azurerm_container_registry" "bitcoin_registry" {
  name                = "bitcoin_registry"
  resource_group_name = module.bitcoin-aks.resource_group_name
  location            = module.bitcoin-aks.location
  sku                 = "Basic"
}