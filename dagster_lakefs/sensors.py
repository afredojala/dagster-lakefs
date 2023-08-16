from dagster import (
    SkipReason,
    run_status_sensor,
    DagsterRunStatus,
    RunStatusSensorContext,
    DefaultSensorStatus,
)

from .resources import LakeFSResource


@run_status_sensor(
    run_status=DagsterRunStatus.SUCCESS, default_status=DefaultSensorStatus.RUNNING
)
def lakefs_branch_delete(context: RunStatusSensorContext, lakefs: LakeFSResource):
    """
    This sensor will commit the output of the job to lakefs
    """
    branch = context.dagster_run.run_id
    if not lakefs._check_if_branch_exists(branch):
        return SkipReason(f"Branch {branch} does not exist")
    lakefs.delete_branch(branch)
