{{ config(materialized="table") }}

with
    unicq_ikan as (
        select 
            id_ikan,
            jenis_ikan,
            harga_ikan,
        from {{ ref("stg_perikanan_indonesia") }}
    )

select 
*
from unicq_ikan
