import os
from lakefs_client import Configuration, models
from lakefs_client.client import LakeFSClient


def get_lakefs_config():
    configuration = Configuration()
    configuration.username = os.getenv("LAKEFS_ACCESS_KEY")
    configuration.password = os.getenv("LAKEFS_SECRET_KEY")
    configuration.host = "http://localhost:8000"
    return configuration


def create_main_branch(configuration):
    client = LakeFSClient(configuration)
    repo = models.RepositoryCreation(
        name="example-repo",
        storage_namespace="local://example-bucket/repos/example-repo",
        default_branch="main",
    )


if __name__ == "__main__":
    config = get_lakefs_config()
    create_main_branch(config)
