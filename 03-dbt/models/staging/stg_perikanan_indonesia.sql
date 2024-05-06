{{
    config(
        materialized='view'
    )
}}

with 

source as (

    select * from {{ source('staging', 'perikanan_indo_data') }}

),

renamed as (

    select

         -- provinsi information
         {{ dbt_utils.generate_surrogate_key(['provinsi']) }} as provinsi_id,  
        id as provinsi_tahun,
        provinsi,
        tahun,

        -- ikan information
        id_ikan,
        jenis_ikan,
        jenis_usaha,
        volume_produksi,
        nilai_produksi,
        angka_konsumsi_ikan,
        harga_ikan

    from source
)

select * from renamed