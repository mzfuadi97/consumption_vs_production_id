{{ config(materialized="table") }}

with
    provinsi as (
        select 
            provinsi_id,
            provinsi,
        from {{ ref("stg_perikanan_indonesia") }}
    )

select 
*
from provinsi
