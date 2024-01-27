# aks-helm-deployment

## Introduction
This section guides you through the deployment of the application to the Azure Kubernetes Service (AKS) using Helm. Ensure that you have completed the prerequisites and setup steps mentioned in the [main readme](../README.md) before proceeding with this deployment.

### Follow the steps below to deploy the application to AKS using Helm:

- 1. Deploy nginx Ingress Controller
```bash
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

- 2. Get External IP of Ingress Controller
```bash
EXTERNAL_ADDRESS=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

 - Verify that the EXTERNAL_ADDRESS was extracted correctly this may take a few minutes until the external IP is assigned
```bash
    echo $EXTERNAL_ADDRESS
```

- 3. Package the Helm Charts
```bash
helm package my-chart
```

- 4. Deploy the Helm Charts
```bash
helm install my-chart my-chart-0.1.0.tgz
```

- 5. Check Pod and Ingress Status
```bash
kubectl get pods
```
```bash
kubectl get ingress
```

- 6. Test the Application
After the pods are running, test the application by sending requests to the ingress controller:
```bash
curl http://$EXTERNAL_ADDRESS/service-a
```
```bash
curl http://$EXTERNAL_ADDRESS/service-b
```

# Clean up instructions
You can find the clean up instructions in the main readme file [here](../README.md#clean-up-instructions)
