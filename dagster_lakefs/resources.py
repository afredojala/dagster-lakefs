from typing import Any, Mapping, Union

from dagster import (
    OutputContext,
    ResourceDependency,
    UPathIOManager,
    ConfigurableIOManager,
    InitResourceContext,
    ConfigurableResource,
)
from lakefs_client import Configuration, models
from lakefs_client.client import LakeFSClient
import polars as pl
from polars import DataFrame
from pydantic import PrivateAttr
from upath import UPath


class LakeFSResource(ConfigurableResource):
    access_key: str
    access_secret: str
    host: str
    repo: str

    def _get_lakefs_client(self) -> LakeFSClient:
        configuration = Configuration()
        configuration.username = self.access_key
        configuration.password = self.access_secret
        configuration.host = self.host
        return LakeFSClient(configuration)

    def _create_lakefs_branch(self, branch: str):
        client = self._get_lakefs_client()
        branch_model = models.BranchCreation(name=branch, source="main")
        client.branches_api.create_branch(
            repository=self.repo, branch_creation=branch_model
        )

    def _commit(
        self, branch: str, msg: str, metadata: Union[Mapping[str, Any], None] = None
    ):
        client = self._get_lakefs_client()
        client.commits_api.commit(
            repository=self.repo,
            branch=branch,
            commit_creation=models.CommitCreation(
                message=msg,
                metadata=metadata if metadata is not None else {},
            ),
        )

    def _merge_branch(self, branch):
        client = self._get_lakefs_client()
        client.refs_api.merge_into_branch(
            repository=self.repo, source_ref=branch, destination_branch="main"
        )

    def _check_if_branch_exists(self, branch: str) -> bool:
        client = self._get_lakefs_client()
        try:
            client.branches_api.get_branch(repository=self.repo, branch=branch)
            return True
        except Exception:
            return False

    def delete_branch(self, branch: str):
        client = self._get_lakefs_client()
        client.branches_api.delete_branch(repository=self.repo, branch=branch)


class LakeFSIOManager(ConfigurableIOManager, UPathIOManager):
    lakefs: ResourceDependency[LakeFSResource]
    extension: str = ".parquet"
    _base_path: UPath = PrivateAttr()

    def setup_for_execution(self, context: InitResourceContext) -> None:
        branch = context.run_id
        if not self.lakefs._check_if_branch_exists(branch):
            self.lakefs._create_lakefs_branch(branch)

        self._base_path = UPath(
            f"s3://{self.lakefs.repo}/{branch}",
            endpoint_url=self.lakefs.host,
            key=self.lakefs.access_key,
            secret=self.lakefs.access_secret,
        )

    def dump_to_path(self, context: OutputContext, obj: DataFrame, path: UPath):
        if obj is None:
            return
        branch = context.run_id
        with path.open("wb") as f:
            obj.write_parquet(f)

        commit_msg = f"Committing {context.step_key} to lakefs"
        self.lakefs._commit(branch, commit_msg)
        self.lakefs._merge_branch(branch)

        context.log.info("comitted data to %s", branch)
        context.log.info("Writing to lakefs path %s", path)
        context.log.info(context.step_key)

    def load_from_path(self, context: OutputContext, path: UPath) -> DataFrame:
        context.log.info("Reading from lakefs path %s", path)
        with path.open("rb") as f:
            return pl.read_parquet(f)
