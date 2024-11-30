# Define variables for easier reuse
accountName="datalakestrprod"
accountKey="4n716YZJ8REWHG0QDjki9ouPirN/IBmhPKyOngs4MsXxgT6bp8BW3mezjsqbMfJkttbd5+biSk3CDgHn7xDyfA=="
containerName="ila-accpac"
folderName="raw"

# Find all blobs under the specified folder with 'Cool' tier and set their tier to 'Archive'
# az storage blob list \
#   --account-name "$accountName" \
#   --account-key "$accountKey" \
#   --container-name "$containerName" \
#   --prefix "$folderName" \
#   --query "[?properties.blobTier == 'Hot'].name" \
#   --output tsv | \
#   xargs -I {} -P 50 az storage blob set-tier \
#     --account-name "$accountName" \
#     --account-key "$accountKey" \
#     --container-name "$containerName" \
#     --tier Archive \
#     --name "{}"

# az account set --subscription 3c44ba2d-eba5-4d51-adb8-8614bf03bd29


az storage blob list \
  --account-name "$accountName" \
  --account-key "$accountKey" \
  --container-name "$containerName" \
  --prefix "$folderName" \
  --query "[?length(name) > length('${folderName}')].name" \
  --output tsv | \
  xargs -I {} -P 25 az storage blob set-tier \
    --account-name "$accountName" \
    --account-key "$accountKey" \
    --container-name "$containerName" \
    --tier Archive \
    --name "{}"