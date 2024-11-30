# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
project_id = 'proyecto-fpv-idrl'
storage_client = storage.Client(project = project_id)

# The name for the new bucket
bucket_name = "bucket-video-fpv-idrl"

# Creates the new bucket
def upload_file(blob_name, file_path):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(filename = file_path)