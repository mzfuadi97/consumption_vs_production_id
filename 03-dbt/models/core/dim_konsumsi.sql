{{ config(materialized="table") }}

with
    konsumsi_ikan as (
        select 
            provinsi_tahun,
            provinsi,
            tahun,
            angka_konsumsi_ikan,
        from {{ ref("stg_perikanan_indonesia") }}
    )

select 
*
from konsumsi_ikan
