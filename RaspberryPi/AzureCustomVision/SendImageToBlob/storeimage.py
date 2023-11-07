from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Replace these variables with your own Azure Storage account details
connection_string = "DefaultEndpointsProtocol=https;AccountName=tpkiot;AccountKey=jzWgteV/05tVaUWG9BKprYJPjM5tpJn2Vmvp/jPHiJqcLskQ7bmFrffD/aTgbJpQKEe06V0aNTkt+AStjlKpBA==;EndpointSuffix=core.windows.net"
container_name = "esp32cam"
blob_name = "..."
local_file_path = "..."

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get or create a container
container_client = blob_service_client.get_container_client(container_name)

# Get a blob client
blob_client = container_client.get_blob_client(blob_name)

# Upload the local image to the blob
with open(local_file_path, "rb") as data:
    blob_client.upload_blob(data)

print(f"Image {blob_name} uploaded to {container_name} container.")
