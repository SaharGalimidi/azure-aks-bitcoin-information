#path: azure-aks-bitcoin-information\terraform\modules\aks\outputs.tf
output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.bitcoin-aks.id
}


output "resource_group_id" {
  value = azurerm_resource_group.bitcoin-rg.id
}

output "resource_group_name" {
  value = azurerm_resource_group.bitcoin-rg.name
  
}

output "aks_cluster_role_assignment" {
  value = azurerm_role_assignment.aks_cluster_admin.id
}

output "aks_rbac_admin_role_assignment" {
  value = azurerm_role_assignment.aks_rbac_admin.id
}


output "aks_rbac_reader_role_assignment" {
  value = azurerm_role_assignment.aks_rbac_reader.id
}

output "location" {
  value = azurerm_resource_group.bitcoin-rg.location
}

output "cluster_name" {
  value = azurerm_kubernetes_cluster.bitcoin-aks.name
}

output "principal_id" {
  value = azurerm_kubernetes_cluster.bitcoin-aks.identity[0].principal_id
}