<!-- General setup
1.      Create for yourself Azure account.

Cluster details
1.      Use Azure and AKS.

2.      Set up K8S cluster , with RBAC enabled.

3.      Cluster should have 2 services – A and B.

4.      Cluster should have Ingress controller, redirecting traffic by URL: xxx/service-A or xxx/service-B.

5.      Service-A should not be able to “talk” with Service-B (policy disabled).

6.      For Service A:write a script\application which retrieves the bitcoin value in dollar from an API on the web (you should find one) every minute and prints it, And also every 10 minutes it should print the average value of the last 10 minutes.

General Guideline
1.      Please, consider this as process for setting up “production-ready” cluster by all meaning, the following cluster buildout should be automated and fully repeatable, Pods should utilize liveness and readiness.

2.      Code should be supportable.

3.      Please, share cluster templates and .yaml files as GitHub repo / zip file. -->


# azure-aks-bitcoin-information

## Overview
This project is a simple example of how to create a Kubernetes cluster on Azure using AKS, and how to deploy a simple application that retrieves the bitcoin value in dollar from an API on the web every minute and prints it, And also every 10 minutes it should print the average value of the last 10 minutes.

## Prerequisites
- Azure account
- Azure CLI
- kubectl
- Docker
- Python 3.6 or higher
- Terraform

## Setup
### Create Azure account
Create a free Azure account [here](https://azure.microsoft.com/en-us/free/).

### Install Azure CLI
Install Azure CLI following the instructions [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest).

### Install kubectl
Install kubectl following the instructions [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

### Install Docker
Install Docker following the instructions [here](https://docs.docker.com/install/).

### Install Python
Install Python following the instructions [here](https://www.python.org/downloads/).

### Install Terraform
Install Terraform following the instructions [here](https://learn.hashicorp.com/terraform/getting-started/install.html).

## Create Kubernetes cluster on Azure
### Login to Azure
Login to Azure using the Azure CLI:
```bash
az login
```

### Run Terraform
Run Terraform to create the Kubernetes cluster:
```bash
cd terraform
terraform init
terraform apply --auto-approve -var-file="terraform.tfvars"
```



