# azure-aks-bitcoin-information

## Overview
This project demonstrates the creation of a Kubernetes cluster on Azure using AKS and the deployment of a simple application. The application retrieves the bitcoin value in dollars from an API every minute and prints it. Additionally, every 10 minutes, it prints the average value of the last 10 minutes.

## Prerequisites
- Azure account
- Azure CLI
- kubectl
- Docker
- Python 3.9 or higher
- Terraform
- Helm

## Setup
### Create Azure account
Create a free Azure account [here](https://azure.microsoft.com/en-us/free/).

### Install Azure CLI
Install Azure CLI following the instructions [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).

### Install kubectl
Install kubectl following the instructions [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

### Install Azure Kubelogin
Install kubelogin following the instructions [here](https://azure.github.io/kubelogin/install.html)

### Install Docker
Install Docker following the instructions [here](https://docs.docker.com/install/).

### Install Python
Install Python following the instructions [here](https://www.python.org/downloads/).

### Install Terraform
Install Terraform following the instructions [here](https://learn.hashicorp.com/terraform/getting-started/install.html).

### Install Helm
Install Helm following the instructions [here](https://helm.sh/docs/intro/install/).

## Note
- The commands in this README are written for a Linux environment. If you are using a different operating system, you may need to adjust the commands accordingly.

## Deploy services to AKS manually using terraform and kubectl
1. **Create Kubernetes cluster on Azure with Terraform:**
   - Connect to your Azure account using the Azure CLI.
     ```bash
     az login
     ```

    - Run Terraform to create the infrastructure, including the Azure Container Registry (ACR) and the Azure Kubernetes Service (AKS) cluster.
      ```bash
        cd terraform
      ```
    - Download the Azure provider and initialize Terraform
      ```bash
        terraform init
      ```
    - See the deployment plan before applying it
      ```bash
        terraform plan -var-file="variables.tfvars"
      ```

    - Apply the deployment plan
      ```bash
        terraform apply --auto-approve -var-file="variables.tfvars" | tee terraform_output.txt
      ```

     Time for a coffee break! terraform apply will take a few minutes to complete.

    - After Terraform has provisioned the ACR and AKS cluster, update the .kube/config file with the credentials of your AKS cluster.
      ```bash
        RG_NAME=$(grep -oP -m 1 'resource_group_name\s+=\s+"\K[^"]+' terraform_output.txt)
      ```

      ```bash
        CLUSTER_NAME=$(grep -oP -m 1 'cluster_name\s+=\s+"\K[^"]+' terraform_output.txt)
      ```

      ```bash
        az aks get-credentials --resource-group $RG_NAME --name $CLUSTER_NAME
      ```
      press y to continue

      ```bash
        ACR_NAME=$(grep -oP -m 1 'acr_name\s+=\s+"\K[^"]+' terraform_output.txt | tr '[:upper:]' '[:lower:]')
      ```

2. **Build and Push Docker Image Locally:**
   - After Terraform has provisioned the ACR, use Docker commands to build your Docker image locally and push it to the Azure Container Registry.

  - Log in to Azure Container Registry
     ```bash
     az acr login --name $ACR_NAME
     ```
  - Build Docker images ( make sure you are in the root directory (i.e. azure-aks-bitcoin-information))
     ```bash
      cd .. 
      ```
      ```bash
      docker build -t $ACR_NAME.azurecr.io/service-a:latest service-a/.
      ```
      ```bash
      docker build -t $ACR_NAME.azurecr.io/service-b:latest service-b/.
      ```
  - Push Docker images to ACR
      ```bash
        docker push $ACR_NAME.azurecr.io/service-a:latest
      ```
      ```bash
        docker push $ACR_NAME.azurecr.io/service-b:latest
      ```

# Manual Deployment using kubectl
Follow the steps in the [aks-manual-deployment](aks-manual-deployment/README.md) directory to deploy the application to AKS using kubectl.

# Deployment using Helm
Follow the steps in the [aks-helm-deployment](my-chart/README.md) directory to deploy the application to AKS using Helm.

### Clean up resources using terraform

  **Destroy Terraform Resources:**
   - Destroy the Terraform-managed resources to delete the AKS cluster and Azure Container Registry.
     ```bash
     # Navigate to the terraform directory
     cd terraform
     # Destroy Terraform resources
     terraform destroy --auto-approve -var-file="variables.tfvars"
     ```
