# azure-aks-bitcoin-information

## Overview
This project demonstrates the creation of a Kubernetes cluster on Azure using AKS and the deployment of a simple application. The application retrieves the bitcoin value in dollars from an API every minute and prints it. Additionally, every 10 minutes, it prints the average value of the last 10 minutes.

## Prerequisites
- Azure account
- Azure CLI
- kubectl
- Docker
- Python 3.6 or higher
- Terraform
- Helm

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

### Install Helm
Install Helm following the instructions [here](https://helm.sh/docs/intro/install/).

## Build and Push Docker Image to Azure Container Registry
1. **Create Kubernetes cluster on Azure with Terraform:**
   - Run Terraform to create the infrastructure, including the Azure Container Registry (ACR) and the Azure Kubernetes Service (AKS) cluster.
     ```bash
     cd terraform
     terraform init
     terraform apply --auto-approve -var-file="variables.tfvars" | tee terraform_output.txt
     ```
   - Extract the ACR name from the Terraform output:
     ```bash
     ACR_NAME=$(grep -oP -m 1 'acr_name\s+=\s+"\K[^"]+' terraform_output.txt)
     ```

2. **Build and Push Docker Image Locally:**
   - After Terraform has provisioned the ACR, use Docker commands to build your Docker image locally and push it to the Azure Container Registry.
     ```bash
     # Log in to Azure Container Registry
     az acr login --name $ACR_NAME

     # Build Docker image
     cd ..
     cd service-a
     docker build -t $ACR_NAME.azurecr.io/your-image:tag .
     cd ..
     cd service-b
     docker build -t $ACR_NAME.azurecr.io/your-image:tag .
     # Push Docker images to ACR
     docker push $ACR_NAME.azurecr.io/your-image:tag
     ```

3. **Deploy Application with Helm:**
   - After pushing the Docker image to the Azure Container Registry and creating the AKS cluster, use Helm to deploy your application.
     ```bash
     # Deploy application with Helm
     cd ..
     helm install my-release ./charts/service-a/
     helm install my-release ./charts/service-b/
     ```

## Cleanup
- Ensure that you clean up resources after testing or when they are no longer needed.

1. **Delete Helm Release:**
   - Delete the Helm release to uninstall the deployed application.
     ```bash
     # Delete Helm release
     helm uninstall my-release
     ```

2. **Destroy Terraform Resources:**
   - Destroy the Terraform-managed resources to delete the AKS cluster and Azure Container Registry.
     ```bash
     # Navigate to the terraform directory
     cd terraform
     # Destroy Terraform resources
     terraform destroy --auto-approve -var-file="variables.tfvars"
     ```

3. **Delete Docker Image from Azure Container Registry (Optional):**
   - If you want to remove the Docker image from the Azure Container Registry, you can do so using the Azure CLI.
     ```bash
     # Delete Docker image from ACR (optional)
     az acr repository delete --name $ACR_NAME --repository your-image --yes
     ```

4. **Remove Local Docker Image (Optional):**
   - Optionally, remove the locally built Docker image.
     ```bash
     # Remove local Docker image (optional)
     docker rmi $ACR_NAME.azurecr.io/your-image:tag
     ```

## Additional Notes
- Ensure that the necessary infrastructure (ACR, AKS) is in place before deploying your application.
- Consider dependencies and ensure each step completes successfully before moving to the next one.
- Include error handling and rollback procedures in case any step encounters issues.
- Update the placeholder values in commands and configurations with your specific details.
- Refer to individual directories for more specific information on Helm charts, Dockerfiles, and Terraform configurations.
