Challenge 05 - Dynatrace Problem Notification and Remediation - Coach's Guide 

[< Previous Solution](./Solution-04.md) - **[Home](../README.md)** - [Next Solution >](./Solution-06.md)

## Solution

### Step 1: Create a custom event in Dynatrace
1. Log in to your Dynatrace account and select the environment you want to work with.
2. Go to **Settings** > **Anomaly detection** > **Custom events** and click **Create custom event**.
3. Give your custom event a meaningful name and description.
4. Choose the severity level for the custom event.
5. In the **Conditions** section, define when the custom event should be triggered. You can set conditions based on metrics, log files, or external events.
6. Save the custom event.

### Step 2: Set up a remediation action that will fix the problem automatically
1. Go to **Settings** > **Anomaly detection** > **Automated response** and click **Create remediation action**.
2. Choose the action type that you want to perform. Dynatrace provides many built-in actions, such as running a script, restarting a process, or scaling a Kubernetes deployment.
3. Provide any necessary parameters for the action.
4. In the **Conditions** section, choose the custom event you created in Step 1 as the trigger for the remediation action.
5. Save the remediation action.

## Troubleshooting
- Make sure that you have the appropriate permissions to create custom events and remediation actions in Dynatrace.
- If the remediation action doesn't trigger when the custom event is detected, check the conditions and parameters for the action to make sure they are correct.
- If you are having trouble setting up the custom event or remediation action, refer to the Dynatrace documentation or contact their support team for assistance.