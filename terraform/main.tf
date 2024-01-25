# path: azure-aks-bitcoin-information\terraform\main.tf
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
  role_definition_name = var.role_definition_name
  role_based_access_control_enabled = var.role_based_access_control_enabled
}

resource "azurerm_container_registry" "bitcoin_registry" {
  name                = "bitcoinRegistry"
  resource_group_name = module.bitcoin-aks.resource_group_name
  location            = module.bitcoin-aks.location
  sku                 = "Basic"
}

data "azurerm_client_config" "current" {}


resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.bitcoin_registry.id
  role_definition_name = "AcrPull"
  principal_id         = data.azurerm_client_config.current.object_id
}
resource "azurerm_role_assignment" "aks_cluster_admin" {
  scope                = module.bitcoin-aks.aks_cluster_id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "regestry_contributor" {
  scope                = azurerm_container_registry.bitcoin_registry.id
  role_definition_name = "Contributor"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "aks_pull_acr" {
  scope                = azurerm_container_registry.bitcoin_registry.id
  role_definition_name = "Contributor"
  principal_id         = module.bitcoin-aks.principal_id
}