Challenge 01 - OneAgent Observability on Azure VM - Coach's Guide 

[< Previous Solution](./Challenge-00.md) - **[Home](../README.md)** - [Next Solution >](./Challenge-02.md)

## Notes & Guidance

1. In order to follow this guide, you need to have an active Dynatrace tenant with an environment ID and an API token with the "Write configuration" permission. If you do not have a Dynatrace tenant, you can sign up for a free trial at [https://www.dynatrace.com/trial/](https://www.dynatrace.com/trial/).
2. This guide assumes that you have already created an Azure VM that you want to monitor with Dynatrace.
3. The Dynatrace OneAgent extension can be installed on both Windows and Linux VMs.

## Step-by-Step Instructions

1. Log in to the Azure portal at [https://portal.azure.com](https://portal.azure.com).
2. Select the virtual machine that you want to monitor with Dynatrace.
3. Click on the **Extensions** tab from the left-hand menu.
4. Click on the **Add** button and search for **Dynatrace OneAgent**.
5. Select **Dynatrace OneAgent** from the list of available extensions and click **Create**.
6. In the **Dynatrace OneAgent** pane, configure the following settings:
   - **Dynatrace Environment ID:** Enter the environment ID of your Dynatrace tenant.
   - **Dynatrace API Token:** Enter an API token with the **Write configuration** permission.
   - **OneAgent Installer Download URL:** Enter the URL of the OneAgent installer for your platform. You can find the installer URL in your Dynatrace tenant under **Deploy Dynatrace > Start installation > OneAgent > Copy installer link**.
   - **Linux OneAgent Installation Command:** If you are installing the OneAgent on a Linux VM, enter the command to install the OneAgent on your distribution. You can find the installation command in your Dynatrace tenant under **Deploy Dynatrace > Start installation > OneAgent > Linux**.
7. Click **OK** to start the extension installation process.
8. Wait for the installation to complete. This may take several minutes.
9. Navigate to your Dynatrace tenant and verify that the VM is being monitored. You should see the Azure VM listed under **Hosts** in the Dynatrace UI.

## Troubleshooting

- If the extension installation fails, check the installation logs in the Azure portal for more information.
- If you are using a Linux VM and the OneAgent installation command is not compatible with your distribution, try using a different installation method, such as the OneAgent installation script or package manager integration. You can find more information in the Dynatrace OneAgent documentation.