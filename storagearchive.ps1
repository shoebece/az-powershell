# Initialize these variables with your values.
$rgName = "rg-ba-lake-prod-uaenorth"
$accountName = "datalakestrprod"
$containerName = "dynamics-crmzms"
$folderName = "raw/"

$ctx = (Get-AzStorageAccount -ResourceGroupName $rgName -Name $accountName).Context

$blobCount = 0
$Token = $Null
$MaxReturn = 5000

do {
    $Blobs = Get-AzStorageBlob -Context $ctx -Container $containerName -Prefix $folderName -MaxCount $MaxReturn -ContinuationToken $Token
    if($Blobs -eq $Null) { break }
    #Set-StrictMode will cause Get-AzureStorageBlob returns result in different data types when there is only one blob
    if($Blobs.GetType().Name -eq "AzureStorageBlob")
    {
        $Token = $Null
    }
    else
    {
        $Token = $Blobs[$Blobs.Count - 1].ContinuationToken;
    }
    $Blobs | ForEach-Object {
            if(($_.BlobType -eq "BlockBlob") -and ($_.AccessTier -eq "Archive") ) {
                $_.BlobClient.SetAccessTier("Hot", $null, "Standard")
            }
        }
}
While ($Token -ne $Null)