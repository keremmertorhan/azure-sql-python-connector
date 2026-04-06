$SubscriptionId = 'YOUR_SUBSCRIPTION_ID_HERE'
$resourceGroupName = "lab8-resourcegroup-$(Get-Random)"
$location = "polandcentral"

$adminSqlLogin = "keremadmin"
$password = "YourStrongPassword123!"

$serverName = "lab8-dbserver-$(Get-Random)"
$databaseName = "lab8-database"

$startIp = "0.0.0.0"
$endIp = "255.255.255.255"

Set-AzContext -SubscriptionId $subscriptionId 

$resourceGroup = New-AzResourceGroup -Name $resourceGroupName -Location $location

$server = New-AzSqlServer -ResourceGroupName $resourceGroupName `
    -ServerName $serverName `
    -Location $location `
    -SqlAdministratorCredentials $(New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $adminSqlLogin, $(ConvertTo-SecureString -String $password -AsPlainText -Force))

$serverFirewallRule = New-AzSqlServerFirewallRule -ResourceGroupName $resourceGroupName `
    -ServerName $serverName `
    -FirewallRuleName "AllowedIPs" -StartIpAddress $startIp -EndIpAddress $endIp

$database = New-AzSqlDatabase -ResourceGroupName $resourceGroupName `
    -ServerName $serverName `
    -DatabaseName $databaseName `
    -RequestedServiceObjectiveName "S0" `
    -SampleName "AdventureWorksLT"

Write-Host "To remove database use command: Remove-AzResourceGroup -ResourceGroupName $resourceGroupName "
