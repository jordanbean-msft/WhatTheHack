# What The Hack - Logic Apps Enterprise Integration

## Introduction

This hack will help you understand how to use Logic Apps to integrate your enterprise systems with other systems and services.  You will learn how to use Logic Apps to connect to other Azure services.  You will also learn how to use Logic Apps to orchestrate complex workflows and business processes.

## Learning Objectives

In this hack you will learn how to:

- Expose a REST API endpoint for users to call
- Injest data from a JSON file into Azure Storage
- Write data to Azure SQL
- Modularize & add validation to your Logic App
- Integrate with Service Bus
- Monitor end-to-end workflows
- Authenticate with AzureAD when calling a custom API
- Author Logic Apps in Visual Studio Code

## Challenges

- Challenge 00: **[Prerequisites - Ready, Set, GO!](Student/Challenge-00.md)**
	 - Prepare your workstation to work with Azure.
- Challenge 01: **[Process JSON input data & write to Storage](Student/Challenge-01.md)**
	 - Create a Logic App workflow to proces JSON input data & write it to Blob Storage
- Challenge 02: **[Write to SQL](Student/Challenge-02.md)**
	 - Add the ability to write data to SQL
- Challenge 03: **[Modularize & integrate with Service Bus](Student/Challenge-03.md)**
	 - Break up the Logic App into smaller pieces & integrate with Service Bus
- Challenge 04: **[Monitor end-to-end workflow](Student/Challenge-04.md)**
	 - Use correlation ID & Application Insights to monitor the end-to-end workflow
- Challenge 05: **[Validation & custom response](Student/Challenge-05.md)**
	 - Add validation & custom responses to the Logic App
- Challenge 06: **[Parameterize with app settings](Student/Challenge-06.md)**
	 - Parameterize the Logic App with app settings instead of hard-coding values
- Challenge 07: **[Authenticate with AzureAD when calling custom API](Student/Challenge-07.md)**
	 - Call a custom API protected via OAuth2 & AzureAD
- Challenge 08: **[Visual Studio Code authoring](Student/Challenge-08.md)**
	 - Author Logic Apps in Visual Studio Code

## Prerequisites

- Your own Azure subscription with Owner access
- Visual Studio Code
- Azure CLI

## Contributors

- Jordan Bean
