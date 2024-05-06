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
    Template for loading data from API
    """
    def download_data(tahun, jenis_val):
        url = f"https://statistik.kkp.go.id/service/download_excel_eksim.php?jns_val={jenis_val}&komoditas_val=Bawal%2CCatfish%2CCumi-Sotong-Gurita%2CKekerangan%2CKerapu%2CKomoditas+Lainnya%2CLayur-Gulama-Reeve+S+Croakers-Bigeye+Croakers+%2CLobster%2CMakarel%2CMutiara%2CRajungan-Kepiting%2CRumput+Laut+%2CSarden-Sardinella%2CSidat%2CTepung+Ikan-Pellet-Makanan+Ikan%2CTilapia%2CTuna-Tongkol-Cakalang%2CUbur-Ubur%2CUdang&tahun_val={tahun}"
        filename = f"data_{jenis_val.lower()}_{tahun}.html"

        # Melakukan request untuk mengunduh data
        response = requests.get(url)

        # Memastikan response sukses (status code 200)
        if response.status_code == 200:
            # Menyimpan data ke dalam file HTML
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Data untuk tahun {tahun} dengan jenis {jenis_val} berhasil diunduh dan disimpan dalam file {filename}")
        else:
            print(f"Gagal mengunduh data untuk tahun {tahun} dengan jenis {jenis_val}")

    def html_to_dataframe(html_file, tahun, jenis_val):
        with open(html_file, 'r') as f:
            html_content = f.read()

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Menemukan tabel dalam HTML
        table = soup.find('table')

        # Membaca tabel HTML ke dalam dataframe
        df = pd.read_html(str(table), header=0)[0]

        # Menambahkan kolom tahun dan jenis_val
        df['Tahun'] = tahun
        df['Jenis_Val'] = jenis_val

        # Mengganti nama kolom sesuai permintaan
        df.rename(columns={f"{tahun}": "Volume (KG)", f"{tahun}.1": "Nilai (USD)"}, inplace=True)

        return df

    # Tahun dan jenis_val yang akan digunakan
    tahun_awal = 2019
    tahun_akhir = 2022
    jenis_val_list = ["Impor", "Ekspor"]

    dfs = []  # List untuk menyimpan semua dataframe

    # Mendownload dan membaca data setiap tahun dan jenis_val
    for tahun in range(tahun_awal, tahun_akhir + 1):
        for jenis_val in jenis_val_list:
            download_data(tahun, jenis_val)
            filename = f"data_{jenis_val.lower()}_{tahun}.html"
            try:
                df = html_to_dataframe(filename, tahun, jenis_val)
                dfs.append(df)
                print(f"Dataframe untuk tahun {tahun} dengan jenis {jenis_val} berhasil dimuat.")
            except Exception as e:
                print(f"Gagal memuat dataframe untuk tahun {tahun} dengan jenis {jenis_val}. Kesalahan: {e}")

    files_to_delete = ["data_impor_2019.html", "data_impor_2020.html", "data_impor_2021.html","data_impor_2022.html","data_ekspor_2019.html","data_ekspor_2020.html","data_ekspor_2021.html","data_ekspor_2022.html" ]

        # Menghapus setiap file dalam daftar
    for file_name in files_to_delete:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File '{file_name}' berhasil dihapus.")
        else:
            print(f"File '{file_name}' tidak ditemukan.")
    # Menggabungkan semua dataframe menjadi satu dataframe tunggal
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.drop(combined_df.index[0])
    combined_df = combined_df.rename(columns=lambda x: x.lower().replace(' ', '_'))
    print("\nDataframe gabungan:")
    print(combined_df.info())
