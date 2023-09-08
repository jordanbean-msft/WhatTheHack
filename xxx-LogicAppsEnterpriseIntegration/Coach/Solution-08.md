# Challenge 08 - Visual Studio Code authoring - Coach's Guide 

[< Previous Solution](./Solution-07.md) - **[Home](./README.md)**

## Notes & Guidance

### Confirm Installation Steps

#### 1. Dotnet Version

![Dotnet](Solution-08/8-Install-Dotnet.png)

#### 2. Function Tools

![Function Tools](Solution-08/8-Install-Func.png)

#### 3. VSCode Extensions

![Extensions](Solution-08/8-Install-Extensions.png)


### Use Local Designer

#### 1. Open Workflow

![Extensions](Solution-08/8-View-Designer.png)

#### 2. Edit Workflow

![Extensions](Solution-08/8-View-Designer-Edit.png)

### Run Locally


#### 1. Update connections for keys

1. Copy existing "connections.json" to "connections.azure.json":
2. Update "connections.json" to use key based authentication instead of managed identity.

**Example SQL Configuration**

```bash

"sql": {
      "parameterValues": {
        "connectionString": "@appsetting('sql_connectionString')"
      },
      "parameterSetName": "connectionString",
      "serviceProvider": {
        "id": "/serviceProviders/sql"
      },
      "displayName": "sqlserver"
    }

```

#### 2. Create "local.settings.json"

Use the "local.settings.json" to configure secrets: 

```json

{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "dotnet",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AzureBlob_connectionString": "",
    "serviceBus_connectionString": "",
    "sql_connectionString": ""
  }
}

```

NOTE: Exclude this file from source control.

#### 3. Launch Workflow

![Launch](Solution-08/8-Run-Debugger.png)

#### 4. Get HTTP trigger URL via overview 

#### 5. Invoke via rest client

![Invoke HTTP Tigger](Solution-08/8-Run-InvokeHTTP.png)

```bash
az aks get-credentials --admin --name aks-rutzsco-aks-001 --resource-group rutzsco-aks-001
```

## Reference

[Run, test, and debug locally](https://learn.microsoft.com/en-us/azure/logic-apps/create-single-tenant-workflows-visual-studio-code#run-test-and-debug-locally)