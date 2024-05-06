if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np

@transformer
def transform(data,data_2,data_3, *args, **kwargs):
    
    df = pd.merge(data,data_2,on="id",how="left")
    df = pd.merge(df,data_3,on="id_ikan",how="left")
    df = df.drop(columns=['tahun_y','nama_ikan','jenis'])
    df.rename(columns={"tahun_x": "tahun"}, inplace=True)
    schema = {
    "jenis_usaha": str,
    "provinsi": str,
    "jenis_ikan": str,
    "tahun": pd.Int64Dtype(),
    "volume_produksi": pd.Int64Dtype(),
    "nilai_produksi": pd.Int64Dtype(),
    "id":str,
    "id_ikan":str,
    "angka_konsumsi_ikan":pd.Int64Dtype(),
    "harga_ikan":float
    }   
    df = df.drop_duplicates(subset=['id','id_ikan'])
    for column, dtype in schema.items():
        if pd.api.types.is_string_dtype(df[column]):
            print(f'string detected for [{column}], skipping...')
            continue
        try:
            if column == "sale_price" and df[column].dtype == "float64":
                df[column] = df[column].round().astype(pd.Int64Dtype())
                print(f'[{column}] converted from {df[column].dtype} to type {dtype}...')
            else:
                df[column] = df[column].astype(dtype)
                print(f'[{column}] converted from {df[column].dtype} to type {dtype}...')
        except (ValueError, TypeError) as e:
            print(f"Warning: Failed to convert column '{column}' to type '{dtype}'. Error: {e}")

    print('\n')
    df.info()
    return df