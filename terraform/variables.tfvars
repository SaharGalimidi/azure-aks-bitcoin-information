# path: azure-aks-bitcoin-information\terraform\variables.tfvars
resource_group_name = "aks-bitcoin-rg"
location            = "eastus"
cluster_name        = "aks-bitcoin-cluster"
dns_prefix          = "aks-bitcoin-dns"
registry_name       = "bitcoinRegistry" #only alphanumeric characters
