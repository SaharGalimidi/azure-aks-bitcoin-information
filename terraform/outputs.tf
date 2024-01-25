# path: azure-aks-bitcoin-information\terraform\outputs.tfs
output "resource_group_id" {
  value = module.bitcoin-aks.resource_group_id
}

output "aks_cluster_id" {
  value = module.bitcoin-aks.aks_cluster_id
}

output "aks_cluster_name" {
  value = module.bitcoin-aks.cluster_name
}

output "resource_group_name" {
  value = module.bitcoin-aks.resource_group_name
}

output "location" {
  value = module.bitcoin-aks.location
}

output "acr_name" {
  value = azurerm_container_registry.bitcoin_registry.name
}

output "acr_login_server" {
  value = azurerm_container_registry.bitcoin_registry.login_server
}

