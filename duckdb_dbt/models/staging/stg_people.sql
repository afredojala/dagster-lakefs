{{ config(materialized="external", location="s3://example-repo/"+var('branch')+"/staging/stg_people.parquet")}}
select * from {{ source('faker', 'fake_data') }}


