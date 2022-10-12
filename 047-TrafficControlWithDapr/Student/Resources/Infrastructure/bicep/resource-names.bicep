param appName string
param region string
param env string

output appInsightsName string = 'ai-${appName}-${region}-${env}'
output logAnalyticsWorkspaceName string = 'la-${appName}-${region}-${env}'
output keyVaultName string = 'kv-${appName}-${region}-${env}'
output storageAccountName string = toLower('sa${appName}${region}${env}')
output serviceBusNamespaceName string = 'sb-${appName}-${region}-${env}'
output iotHubName string = 'iotHub-${appName}-${region}-${env}'
output aksName string = 'aks-${appName}-${region}-${env}'
output containerRegistryName string = toLower('cr${appName}${region}${env}')
output logicAppName string = 'logic-smtp-${appName}-${region}-${env}'
output redisCacheName string = 'redis-${appName}-${region}-${env}'
output storageAccountEntryCamContainerName string = 'trafficcontrol-entrycam'
output storageAccountExitCamContainerName string = 'trafficcontrol-exitcam'
output eventHubEntryCamName string = 'entrycam'
output eventHubExitCamName string = 'exitcam'
output eventHubNamespaceName string = 'ehn-trafficcontrol-${appName}-${region}-${env}'
output eventHubConsumerGroupName string = 'trafficcontrolservice'
output eventHubListenAuthorizationRuleName string = 'listen'