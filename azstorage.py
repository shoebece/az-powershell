import csv
from azure.storage.filedatalake import DataLakeServiceClient

# Azure Data Lake configuration
storage_account_name = "strgdatalakearchive"  # Replace with your storage account name
storage_account_key = "4n716YZJ8REWHG0QDjki9ouPirN/IBmhPKyOngs4MsXxgT6bp8BW3mezjsqbMfJkttbd5+biSk3CDgHn7xDyfA=="    # Replace with your storage account access key

# Create a DataLakeServiceClient using the storage account key
service_client = DataLakeServiceClient(
    account_url=f"https://{storage_account_name}.dfs.core.windows.net",
    credential=storage_account_key
)

def list_folders(container_client, path=""):
    items = []
    paths = container_client.get_paths(path=path)

    for p in paths:
        # Only add directories (folders), excluding files
        if p.is_directory:
            item = {
                "container": container_client.file_system_name,
                "path": p.name,
                "is_directory": p.is_directory
            }
            items.append(item)
            
            # Recursively add subdirectories
            items.extend(list_folders(container_client, path=p.name))

    return items

# Retrieve all containers and their folder contents
def export_containers_to_csv(filename="containers_and_folders.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Container", "Path", "Is Directory"])
        
        # Iterate over all containers in the storage account
        containers = service_client.list_file_systems()
        
        for container in containers:
            container_client = service_client.get_file_system_client(container.name)
            items = list_folders(container_client)
            
            # Write each item (only folders) to the CSV file
            for item in items:
                writer.writerow([item["container"], item["path"], item["is_directory"]])

# Run the export function
export_containers_to_csv()
print("Export completed successfully.")