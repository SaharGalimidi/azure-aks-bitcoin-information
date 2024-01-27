# aks-manual-deployment

## Introduction
This section guides you through the manual deployment of the application to the Azure Kubernetes Service (AKS) using kubectl. Ensure that you have completed the prerequisites and setup steps mentioned in the [main readme](../README.md) before proceeding with this manual deployment.

### Follow the steps below to deploy the application to AKS using kubectl:

- 1. Deploy nginx Ingress Controller
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```
- 2. Get External IP of Ingress Controller
```bash
EXTERNAL_ADDRESS=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
```

 - Verify that the EXTERNAL_ADDRESS was extracted correctly this may take a few minutes until the external IP is assigned
```bash
    echo $EXTERNAL_ADDRESS
```

- 3. Deploy Services, Policy and Ingress Rules
```bash
kubectl apply -f aks-manual-deployment/ingress/ingress.yaml
```
```bash
kubectl apply -f aks-manual-deployment/service-a/serviceA-deployment.yaml
```
```bash
kubectl apply -f aks-manual-deployment/service-b/serviceB-deployment.yaml
```
```bash
kubectl apply -f aks-manual-deployment/network-policy/network-policy.yaml
```

- 4. Check Pod and Ingress Status
```bash
kubectl get pods
```
```bash
kubectl get ingress
```

- 5. Test the Application
After the pods are running, test the application by sending requests to the ingress controller:
```bash
curl http://$EXTERNAL_ADDRESS/service-a
```
```bash
curl http://$EXTERNAL_ADDRESS/service-b
```
