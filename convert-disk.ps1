# Define the Resource Group name
$resourceGroupName = "Rgsaphanaprod"

# Login to Azure account (if not already logged in)
Connect-AzAccount

$disks = Get-AzDisk -ResourceGroupName $resourceGroupName

# Loop through each disk to check and change SKU if necessary
foreach ($disk in $disks) {
    # Check if the disk's SKU is Premium (to change it to Standard HDD)
    if ($disk.Sku.Name -eq "Premium_LRS") {
        Write-Output "Changing SKU for disk $($disk.Name) from Premium to Standard HDD"

        # Update the SKU to Standard HDD
        $disk.Sku.Name = "Standard_LRS"

        # Update the disk with the new SKU
        Update-AzDisk -Disk $disk -ResourceGroupName $resourceGroupName -DiskName $disk.Name
        Write-Output "SKU for disk $($disk.Name) updated successfully."
    } else {
        Write-Output "Disk $($disk.Name) is already set to $($disk.Sku.Name), no changes needed."
    }
}