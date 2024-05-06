import io
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Fetches data from Socrata API in chunks defined by "limit" and combines them into a DataFrame.
    Returns:
      pd.DataFrame: Combined DataFrame containing all data.
    """

    def download_data(tahun):
        url = f"https://statistik.kkp.go.id/service/download_excel_prod_ikan_prov.php?jns_prod_val=&jns_ikan_val=&tahun_val={tahun}&prov_val="
        filename = f"produksi_ikan_{tahun}.xlsx"

        # Melakukan request untuk mengunduh data
        response = requests.get(url)

        # Memastikan response sukses (status code 200)
        if response.status_code == 200:
            # Menyimpan data ke dalam file
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Data produksi ikan Indonesia tahun {tahun} berhasil diunduh dan disimpan dalam file {filename}")
        else:
            print(f"Gagal mengunduh data produksi ikan Indonesia untuk tahun {tahun}")

    def html_to_dataframe(html_file):
        with open(html_file, 'r') as f:
            html_content = f.read()

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Menemukan tabel dalam HTML
        table = soup.find('table')

        # Mengonversi tabel HTML menjadi dataframe
        df = pd.read_html(str(table))[0]

        return df

    tahun = [2019, 2020, 2021, 2022]

    dfs = []  # List untuk menyimpan semua dataframe

    for tahun in tahun:
        download_data(tahun)
        html_file = f"produksi_ikan_{tahun}.xlsx"
        df = html_to_dataframe(html_file)
        dfs.append(df)  # Menambahkan dataframe ke dalam list
        print(f"Data produksi ikan Indonesia tahun {tahun} berhasil terinput")

    # Menggabungkan semua dataframe menjadi satu dataframe tunggal
    combined_df = pd.concat(dfs, ignore_index=True)
    files_to_delete = ["produksi_ikan_2019.xlsx", "produksi_ikan_2020.xlsx", "produksi_ikan_2021.xlsx", "produksi_ikan_2022.xlsx"]

    # Menghapus setiap file dalam daftar
    for file_name in files_to_delete:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File '{file_name}' berhasil dihapus.")
        else:
            print(f"File '{file_name}' tidak ditemukan.")
    combined_df['Tahun'] = combined_df['Tahun'].astype(str)
    combined_df['id'] = combined_df['Tahun'] + '-' + combined_df['Provinsi']
    combined_df.columns = combined_df.columns.str.replace('/', '_')
    combined_df.columns = combined_df.columns.str.replace(' ', '_')
    
    # Mengubah semua nama kolom menjadi huruf kecil
    combined_df.columns = combined_df.columns.str.lower()
    combined_df['id_ikan'] = combined_df['tahun'] + '-' + combined_df['jenis_ikan']
    print(combined_df.info())
    
    return combined_df