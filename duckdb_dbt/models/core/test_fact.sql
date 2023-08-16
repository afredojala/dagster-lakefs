{{ config(materialized='external', location="s3://example-repo/"+var('branch')+"/test_fact.parquet")}}
select job, avg(salary) as av_salary from {{ ref('stg_people') }} group by 1
