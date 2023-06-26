Challenge 02 - Dynatrace Observability on AKS - Coach's Guide

[< Previous Solution](./Solution-01.md) - **[Home](../README.md)** - [Next Solution >](./Solution-03.md)

## Solution Guide

### Step 1: Create an AKS cluster

1. Open the Azure portal and navigate to the AKS service.
2. Click on the "Add" button to create a new AKS cluster.
3. Fill in the required fields, such as the resource group, cluster name, location, and node pool settings.
4. Review and create the cluster.

Alternatively, you can use the Azure CLI to create the AKS cluster. Here is an example command:

```
az aks create --resource-group <resource-group-name> --name <cluster-name> --node-count 1 --generate-ssh-keys
```

### Step 2: Deploy a sample application to the AKS cluster

1. Create a Kubernetes manifest file for the sample application. Here is an example:

```
apiVersion: v1
kind: Pod
metadata:
  name: sample-app
  labels:
    app: sample-app
spec:
  containers:
    - name: sample-app
      image: nginx:latest
      ports:
        - containerPort: 80
```

2. Use `kubectl` command to deploy the Kubernetes manifest to the AKS cluster:

```
kubectl apply -f <path-to-manifest-file>
```

### Step 3: Install the Dynatrace OneAgent Operator on the AKS cluster

1. Follow the instructions in the [Dynatrace documentation](https://www.dynatrace.com/support/help/cloud-platforms/kubernetes/deploy-oneagent-on-kubernetes-with-the-oneagent-operator/) to install the OneAgent Operator using Helm.
2. Retrieve the Dynatrace API token and PaaS token from your Dynatrace account.
3. Create a Kubernetes secret to store the Dynatrace tokens:

```
kubectl create secret generic dynatrace-oneagent --from-literal="apiToken=<API-token>" --from-literal="paasToken=<PaaS-token>"
```

### Step 4: Configure the Dynatrace OneAgent Operator to monitor the sample application

1. Create a Kubernetes manifest file for the Dynatrace OneAgent Operator. Here is an example:

```
apiVersion: dynatrace.com/v1alpha1
kind: OneAgent
metadata:
  name: oneagent
spec:
  apiUrl: https://<your-environment-id>.live.dynatrace.com/api
  tokens:
    apiToken:
      secretName: dynatrace-oneagent
      secretKey: apiToken
    paasToken:
      secretName: dynatrace-oneagent
      secretKey: paasToken
```

2. Use `kubectl` command to deploy the OneAgent Operator manifest to the AKS cluster:

```
kubectl apply -f <path-to-oneagent-manifest-file>
```

3. Create a Kubernetes manifest file for the Dynatrace OneAgent injection. Here is an example:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
spec:
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
      annotations:
        ad.datadoghq.com/sample-app.check_names: '["nginx"]'
        ad.datadoghq.com/sample-app.init_configs: '[{}]'
        ad.datadoghq.com/sample-app.instances: '[{"nginx_status_url": "http://%%host%%:%%port%%/nginx_status"}]'
        oneagent.dynatrace.com/injection: "true"
    spec:
      containers:
        - name: sample-app
          image: nginx:latest
          ports:
            - containerPort