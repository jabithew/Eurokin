from azure.storage.blob import BlobServiceClient
from pathlib import Path
import json, uuid


class azure_blob:
    def __init__(self, secrets: dict) -> BlobServiceClient:
        if {"connect_string"} <= set(secrets):
            self.connect_string = secrets["connect_string"]
        else:
            raise KeyError("Secrets dict must contain connect_string")
        self.service_client = BlobServiceClient.from_connection_string(
            self.connect_string
        )
        self.deliverables = None
        return None

    def get_deliverables_container(self):
        container_list = [
            container.name for container in self.service_client.list_containers()
        ]
        if "deliverables" in set(container_list):
            self.deliverables = self.service_client.get_container_client("deliverables")
        else:
            self.deliverables = self.service_client.create_container("deliverables")

    def upload_deliverable(self, file_path: Path):
        if self.deliverables is None:
            self.get_deliverables_container()
        blob_client = self.deliverables.get_blob_client(blob=file_path.name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)


if __name__ == "__main__":
    cwd = Path().cwd()
    deliverables_dir = cwd / "Deliverables"

    with open("secrets.json") as secrets_file:
        secrets = json.load(secrets_file)
    azure_secrets = secrets["azure"]

    eurokin_azure = azure_blob(azure_secrets)

    deliverables_list = cwd / "deliverables.json"
    eurokin_azure.upload_deliverable(deliverables_list)

    assert False
