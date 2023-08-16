from dagster import asset, OpExecutionContext
from faker import Faker
import polars as pl
from .dbt import all_dbt_assets


def create_fake_data(n: int) -> pl.DataFrame:
    fake = Faker()
    data = [
        {
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email(),
            "job": fake.job(),
            "salary": fake.pyint(),
            "start_date": fake.date(),
            "end_date": fake.date(),
        }
        for _ in range(n)
    ]
    return pl.DataFrame(data)


@asset(key_prefix="faker")
def fake_data(context: OpExecutionContext) -> pl.DataFrame:
    context.log.info(context.run_id)
    return create_fake_data(1000)


@asset
def group_by_job(context: OpExecutionContext, fake_data: pl.DataFrame) -> pl.DataFrame:
    return create_fake_data(1000).groupby("job").agg(pl.sum("salary"))
