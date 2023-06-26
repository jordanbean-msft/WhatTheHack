Challenge 01: OneAgent Observability on Azure VM

[< Previous Challenge](./Challenge-00.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-02.md)

## Introduction

In this challenge, you will learn how to enable OneAgent observability on an Azure VM, allowing Dynatrace to monitor the VM's performance. 

## Description

1. Navigate to the Azure portal and select the virtual machine that you want to monitor with Dynatrace.
2. Select the **Extensions** tab from the left-hand menu.
3. Click on the **Add** button and search for **Dynatrace OneAgent**.
4. Select **Dynatrace OneAgent** from the list of available extensions.
5. Click **Create** to start the extension installation process.
6. In the **Dynatrace OneAgent** pane, configure the following settings:
   - **Dynatrace Environment ID:** The environment ID of your Dynatrace tenant.
   - **Dynatrace API Token:** An API token with the **Write configuration** permission.
   - **OneAgent Installer Download URL:** The URL of the OneAgent installer for your platform.
   - **Linux OneAgent Installation Command:** The command to install the OneAgent on Linux VMs.
7. Click **OK** to start the extension installation process.
8. Wait for the installation to complete. This may take several minutes.
9. Navigate to your Dynatrace tenant and verify that the VM is being monitored.

## Success Criteria

- Verify that the Dynatrace OneAgent is installed on the Azure VM.
- Validate that performance metrics for the VM are being reported to your Dynatrace tenant.

## Learning Resources

- [Azure Virtual Machines documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/)
- [Dynatrace OneAgent documentation](https://www.dynatrace.com/support/help/)
- [Azure Virtual Machines and Dynatrace integration guide](https://www.dynatrace.com/support/help/cloud-platforms/microsoft-azure/how-do-i-monitor-azure-virtual-machines/) 

## Tips

- If you encounter issues with the OneAgent installation, check the installation logs in the Azure portal for more information.
- If you are using a Linux VM, make sure that the OneAgent installation command is compatible with your distribution.