{{
  config(
    materialized='external',
    location="s3://example-repo/"+var('branch')+"/core/test_fact.parquet"
  )
}}
select job, avg(salary) as avg_salary from {{ ref('stg_people') }} group by 1
