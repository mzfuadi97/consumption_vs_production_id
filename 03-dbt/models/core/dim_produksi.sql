{{ config(materialized="table") }}

with
    produksi_ikan as (
        select 
            id_ikan,
            jenis_usaha,
            tahun,
            volume_produksi,
            nilai_produksi
        from {{ ref("stg_perikanan_indonesia") }}
    )

select 
*
from produksi_ikan
