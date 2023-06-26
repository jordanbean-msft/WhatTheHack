Challenge 02: Dynatrace Observability on AKS

[< Previous Challenge](./Challenge-01.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-03.md)

## Introduction

In this challenge, you will learn how to deploy a containerized workload to AKS and monitor it with Dynatrace. AKS is a managed Kubernetes service provided by Azure, making it easy to deploy, scale, and manage containerized applications.

## Description

1. Create an AKS cluster using the Azure portal or Azure CLI.
2. Deploy a sample application to the AKS cluster using a Kubernetes manifest.
3. Install the Dynatrace OneAgent Operator on the AKS cluster.
4. Configure the Dynatrace OneAgent Operator to monitor the sample application.
5. Verify that Dynatrace is monitoring the sample application.

## Success Criteria

- Deploy an AKS cluster using the Azure portal or Azure CLI.
- Deploy a sample application to the AKS cluster using a Kubernetes manifest.
- Install the Dynatrace OneAgent Operator on the AKS cluster.
- Configure the Dynatrace OneAgent Operator to monitor the sample application.
- Verify that Dynatrace is monitoring the sample application.

## Learning Resources

- [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/)
- [Kubernetes Tutorials](https://kubernetes.io/docs/tutorials/)
- [Deploying to Kubernetes](https://docs.docker.com/get-started/kubernetes/)
- [Install Dynatrace OneAgent on Kubernetes](https://www.dynatrace.com/support/help/cloud-platforms/kubernetes/installation-and-operation/full-stack/deploy-oneagent-on-kubernetes/)
- [Dynatrace OneAgent Operator](https://www.dynatrace.com/support/help/technology-support/cloud-platforms/kubernetes/deploy-oneagent-on-kubernetes-with-the-oneagent-operator/)
- [Verify OneAgent injection](https://www.dynatrace.com/support/help/cloud-platforms/kubernetes/installation-and-operation/full-stack/verify-oneagent-injection/)
- [Dynatrace Kubernetes Monitoring](https://www.dynatrace.com/platform/kubernetes/)

## Tips

- Use `kubectl` commands to deploy the Kubernetes manifest to the AKS cluster.
- Verify that the sample application is running on the AKS cluster before installing the OneAgent Operator.
- Use the Dynatrace OneAgent Operator Helm chart to install the OneAgent Operator on the AKS cluster.
- Verify that the Dynatrace OneAgent is monitoring the sample application using the Dynatrace web UI.