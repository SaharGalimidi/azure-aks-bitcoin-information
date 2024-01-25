# path: azure-aks-bitcoin-information\terraform\variables.tfvars
resource_group_name = "aks-bitcoin-rg"
location            = "eastus"
cluster_name        = "aks-bitcoin-cluster"
dns_prefix          = "aks-bitcoin-dns"
role_definition_name = "Azure Kubernetes Service RBAC Cluster Admin"
