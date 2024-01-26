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
  source                            = "./modules/aks"
  cluster_name                      = var.cluster_name
  dns_prefix                        = var.dns_prefix
  location                          = var.location
  resource_group_name               = var.resource_group_name
  role_based_access_control_enabled = var.role_based_access_control_enabled
}


resource "null_resource" "aks_acr_attachment" {

  depends_on = [azurerm_container_registry.bitcoin_registry, module.bitcoin-aks]

  provisioner "local-exec" {
    command = "az aks update -n ${module.bitcoin-aks.cluster_name} -g ${module.bitcoin-aks.resource_group_name} --attach-acr ${azurerm_container_registry.bitcoin_registry.name}"
  }
}


resource "azurerm_container_registry" "bitcoin_registry" {
  name                = var.registry_name
  resource_group_name = module.bitcoin-aks.resource_group_name
  location            = module.bitcoin-aks.location
  sku                 = "Basic"
}

data "azurerm_client_config" "current" {}


resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.bitcoin_registry.id
  role_definition_name = var.role_acr_pull
  principal_id         = data.azurerm_client_config.current.object_id
}
resource "azurerm_role_assignment" "aks_cluster_admin" {
  scope                = module.bitcoin-aks.aks_cluster_id
  role_definition_name = var.role_rbac_cluster_admin
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "regestry_contributor" {
  scope                = azurerm_container_registry.bitcoin_registry.id
  role_definition_name = var.role_registry_contributor
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_role_assignment" "aks_pull_acr" {
  scope                = azurerm_container_registry.bitcoin_registry.id
  role_definition_name = var.role_acr_pull
  principal_id         = module.bitcoin-aks.principal_id
}
