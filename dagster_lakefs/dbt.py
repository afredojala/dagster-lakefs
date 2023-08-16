import json
import os
from pathlib import Path
from dagster import OpExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource

from .resources import LakeFSResource

dbt_project_dir = Path(__file__).joinpath("..", "..", "duckdb_dbt").resolve()
dbt_cli = DbtCliResource(project_dir=os.fspath(dbt_project_dir))
dbt_parse_invocation = dbt_cli.cli(["parse"], manifest={}).wait()
dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")


@dbt_assets(manifest=dbt_manifest_path)
def all_dbt_assets(
    context: OpExecutionContext, dbt: DbtCliResource, lakefs: LakeFSResource
):
    branch = context.run_id
    if not lakefs._check_if_branch_exists(branch):
        lakefs._create_lakefs_branch(branch)
    vars = {"branch": branch}
    dbt_build = dbt.cli(["build", "--vars", json.dumps(vars)], context=context)
    yield from dbt_build.stream()
    run_results = dbt_build.get_artifact("run_results.json")

    materialized_assets = set()
    for run_result in run_results["results"]:
        if run_result["status"] == "success":
            materialized_assets.add(run_result["unique_id"])
    context.log.info(run_results)
    commit_msg = "Committing dbt assets to lakefs"
    context.log.info(materialized_assets)
    lakefs._commit(
        branch, msg=commit_msg, metadata={"assets": ", ".join(materialized_assets)}
    )
