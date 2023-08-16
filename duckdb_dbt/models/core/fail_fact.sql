{{
  config(
    materialized='external',
    location="s3://example-repo/"+var('branch')+"/core/fail_fact.parquet"
  )
}}

select start_date, count(*) as num_records from {{ ref('stg_people') }} group by 1

