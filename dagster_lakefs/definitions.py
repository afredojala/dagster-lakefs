from dagster import Definitions, EnvVar, load_assets_from_modules

from . import assets
from .resources import LakeFSIOManager, LakeFSResource
from .sensors import lakefs_branch_delete
from .dbt import dbt_cli

lakefs = LakeFSResource(
    access_key=EnvVar("LAKEFS_ACCESS_KEY"),
    access_secret=EnvVar("LAKEFS_SECRET_KEY"),
    host="http://localhost:8000",
    repo=EnvVar("LAKEFS_REPO"),
)

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    resources={
        "io_manager": LakeFSIOManager(lakefs=lakefs),
        "dbt": dbt_cli,
        "lakefs": lakefs,
    },
    sensors=[lakefs_branch_delete],
)
