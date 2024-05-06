{{ config(materialized='table') }}

with data_perikanan as (
    select
        provinsi_id,
        id_ikan,
        provinsi_tahun,
        harga_ikan,
        angka_konsumsi_ikan
    from
        {{ ref("stg_perikanan_indonesia") }}
)

select  
        dp.id_ikan,   
        dp.provinsi_id,
        pro.provinsi,
        dpr.jenis_usaha,
        dpr.tahun,
        dpr.volume_produksi,
        dpr.nilai_produksi,
        dp.angka_konsumsi_ikan,
        dp.harga_ikan
from data_perikanan dp
left join 
    {{ ref("dim_produksi") }} dpr ON dp.id_ikan = dpr.id_ikan
left join 
    {{ ref("dim_provinsi") }} pro ON dp.provinsi_id = pro.provinsi_id
