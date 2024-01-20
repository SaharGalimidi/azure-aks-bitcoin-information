output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.bitcoin-aks.id
}


output "resource_group_id" {
  value = azurerm_resource_group.bitcoin-rg.id
}

output "resource_group_name" {
  value = azurerm_resource_group.bitcoin-rg.name
  
}

output "location" {
  value = azurerm_resource_group.bitcoin-rg.location
}