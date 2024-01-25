#path: azure-aks-bitcoin-information\terraform\modules\aks\main.tf
provider "azurerm" {
  features {}
}


resource "azurerm_kubernetes_cluster" "bitcoin-aks" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix
  role_based_access_control_enabled = true
  

  azure_active_directory_role_based_access_control {
    managed             = true
    azure_rbac_enabled = true
  }
  

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }

  depends_on = [ azurerm_resource_group.bitcoin-rg ]
}


resource "azurerm_resource_group" "bitcoin-rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_role_assignment" "aks_cluster_admin" {
  scope                = azurerm_kubernetes_cluster.bitcoin-aks.id
  role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
  principal_id         = azurerm_kubernetes_cluster.bitcoin-aks.identity[0].principal_id
}

resource "azurerm_role_assignment" "aks_rbac_admin" {
  scope                = azurerm_kubernetes_cluster.bitcoin-aks.id
  role_definition_name = "Azure Kubernetes Service RBAC Admin"
  principal_id         = azurerm_kubernetes_cluster.bitcoin-aks.identity[0].principal_id
}
resource "azurerm_role_assignment" "aks_rbac_reader" {
  scope                = azurerm_kubernetes_cluster.bitcoin-aks.id
  role_definition_name = "Azure Kubernetes Service RBAC Reader"
  principal_id         = azurerm_kubernetes_cluster.bitcoin-aks.identity[0].principal_id
}

