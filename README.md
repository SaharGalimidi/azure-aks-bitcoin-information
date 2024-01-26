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

## Build and Push Docker Image to Azure Container Registry
1. **Create Kubernetes cluster on Azure with Terraform:**
   - Connect to your Azure account using the Azure CLI.
     ```bash
     az login
     ```

    - Run Terraform to create the infrastructure, including the Azure Container Registry (ACR) and the Azure Kubernetes Service (AKS) cluster.
      ```bash
        cd terraform
      ```
    - See the deployment plan before applying it
      ```bash
        terraform plan -var-file="variables.tfvars"
      ```
    - Download the Azure provider and initialize Terraform
      ```bash
        terraform init
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

    - Verify that the resource group name and cluster name were extracted correctly
      ```bash
        echo $RG_NAME
      ```

      ```bash
        echo $CLUSTER_NAME
      ```

      ```bash
        az aks get-credentials --resource-group $RG_NAME --name $CLUSTER_NAME
      ```

    - Extract the ACR name from the Terraform output:

      ```bash
        ACR_NAME=$(grep -oP -m 1 'acr_name\s+=\s+"\K[^"]+' terraform_output.txt | tr '[:upper:]' '[:lower:]')
      ```

    - Verify that the ACR name was extracted correctly

      ```bash
        echo $ACR_NAME
      ```

2. **Build and Push Docker Image Locally:**
   - After Terraform has provisioned the ACR, use Docker commands to build your Docker image locally and push it to the Azure Container Registry.
     <!-- ```bash
     # Log in to Azure Container Registry
     az acr login --name $ACR_NAME

     # Build Docker images
     cd .. # make sure you are in the root directory (i.e. azure-aks-bitcoin-information)
     docker build -t $ACR_NAME.azurecr.io/your-image-name:latest service-a/.

     docker build -t $ACR_NAME.azurecr.io/your-image-name:latest service-b/.
     # Push Docker images to ACR 
     docker push $ACR_NAME.azurecr.io/your-image-name:latest
     ``` -->
  - Log in to Azure Container Registry
     ```bash
     az acr login --name $ACR_NAME
     ```
  - Build Docker images
     ```bash
      cd .. # make sure you are in the root directory (i.e. azure-aks-bitcoin-information)
      ```
      ```bash
      docker build -t $ACR_NAME.azurecr.io/your-image-name:latest service-a/.
      ```
      ```bash
      docker build -t $ACR_NAME.azurecr.io/your-image-name:latest service-b/.
      ```
  - Push Docker images to ACR
      ```bash
        docker push $ACR_NAME.azurecr.io/your-image-name:latest
      ```
      
3. **Deploy Application with kubectl:**
   - After pushing the Docker image to the Azure Container Registry and creating the AKS cluster, use kubectl to deploy your application.

   - Deploy nginx ingress controller for the cluster
      source: https://kubernetes.github.io/ingress-nginx/deploy/
     ```bash
      kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
     ```
    - Get the external IP of the ingress controller
     ```bash
      EXTERNAL_ADDRESS=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
     ```
    - Verify that the EXTERNAL_ADDRESS was extracted correctly this may take a few minutes until the external IP is assigned
     ```bash
      echo $EXTERNAL_ADDRESS
     ```
    - Deploy the services and ingress rules to the cluster in the ingress-nginx namespace
       make sure you are in the root directory (i.e. azure-aks-bitcoin-information)
      ```bash
          cd ..
      ```
      
      ```bash
        kubectl apply -f service-a/service-a.yaml
      ```

      ```bash
        kubectl apply -f service-b/service-b.yaml
      ```

      ```bash
        kubectl apply -f ingress-rules/ingress-rules.yaml
      ```
      
    - Check the status of the pods
     ```bash
      kubectl get pods
     ```
    - Check the status of the ingress rules
     ```bash
      kubectl get ingress
     ```

4. **Test the application:**
    - After the pods are running, you can test the application by sending requests to the ingress controller
      ```bash
        curl http://$EXTERNAL_ADDRESS/service-a
      ```
      ```bash
        curl http://$EXTERNAL_ADDRESS/service-b
      ```


5. **Destroy Terraform Resources:**
   - Destroy the Terraform-managed resources to delete the AKS cluster and Azure Container Registry.
     ```bash
     # Navigate to the terraform directory
     cd terraform
     # Destroy Terraform resources
     terraform destroy --auto-approve -var-file="variables.tfvars"
     ```
