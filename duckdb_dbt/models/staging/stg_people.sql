{{ config(materialized="external", location="s3://example-repo/"+var('branch')+"/stg_people.parquet")}}
select * from {{ source('faker', 'fake_data') }}


