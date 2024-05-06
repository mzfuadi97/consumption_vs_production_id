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

    def download_data(no_kpda, jenis):
        url = f"https://statistik.kkp.go.id/service/search_harga_kpda.php?type=excel&no_kpda={no_kpda}"
        filename = f"harga_{jenis}.html"

        # Melakukan request untuk mengunduh data
        response = requests.get(url)

        # Memastikan response sukses (status code 200)
        if response.status_code == 200:
            # Menyimpan data ke dalam file HTML
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Data harga {jenis} berhasil diunduh dan disimpan dalam file {filename}")
        else:
            print(f"Gagal mengunduh data harga {jenis}")

    def html_to_dataframe(html_file):
        with open(html_file, 'r') as f:
            html_content = f.read()

        # Parsing HTML menggunakan BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Menemukan tabel dalam HTML
        table = soup.find('table')

        # Mengonversi tabel HTML menjadi dataframe
        df = pd.read_html(str(table), header=1)[0]  # header=1 untuk menggunakan baris kedua sebagai header kolom

        return df

    # Unduh data untuk perikanan tangkap
    download_data(9001, "perikanan_tangkap")
    # Ubah data HTML menjadi dataframe
    df_perikanan_tangkap = html_to_dataframe("harga_perikanan_tangkap.html")
    print("Dataframe untuk perikanan tangkap:")
    print(df_perikanan_tangkap)

    # Unduh data untuk perikanan budidaya
    download_data(9002, "perikanan_budidaya")
    # Ubah data HTML menjadi dataframe
    df_perikanan_budidaya = html_to_dataframe("harga_perikanan_budidaya.html")
    print("\nDataframe untuk perikanan budidaya:")
    print(df_perikanan_budidaya)

    files_to_delete = ["harga_perikanan_tangkap.html", "harga_perikanan_budidaya.html"]

        # Menghapus setiap file dalam daftar
    for file_name in files_to_delete:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File '{file_name}' berhasil dihapus.")
        else:
            print(f"File '{file_name}' tidak ditemukan.")

    df_perikanan_budidaya = df_perikanan_budidaya.rename(columns=lambda x: x.lower().replace(' ', '_'))
    kolom_baru = {'0':"2018",'0.1': '2019', '0.2': '2020', '0.3': '2021','0.4':"2022"}
    df_perikanan_budidaya = df_perikanan_budidaya.rename(columns={'harga_ikan_perikanan_budidaya_rata-rata_(rp)':"nama_ikan"})
    df_perikanan_budidaya = df_perikanan_budidaya.rename(columns=kolom_baru)
    df_perikanan_budidaya['jenis'] = "perikanan budidaya"
    df_perikanan_tangkap = df_perikanan_tangkap.rename(columns=lambda x: x.lower().replace(' ', '_'))
    df_perikanan_tangkap = df_perikanan_tangkap.rename(columns={'harga_ikan_perikanan_tangkap_rata-rata_(rp)':"nama_ikan"})
    kolom_baru = {'0':"2018",'0.1': '2019', '0.2': '2020', '0.3': '2021','0.4':"2022"}
    df_perikanan_tangkap = df_perikanan_tangkap.rename(columns=kolom_baru)
    df_perikanan_tangkap['jenis'] = "perikanan tangkap"
    df = pd.concat([df_perikanan_budidaya,df_perikanan_tangkap]).reset_index(drop=True)
    df_unpivoted = pd.melt(df, id_vars=['nama_ikan', 'jenis',],
                            var_name='tahun', value_name='harga_ikan')
    df_unpivoted['nama_ikan'] = df_unpivoted['nama_ikan'].str.upper()
    df_unpivoted['id_ikan'] = df_unpivoted["tahun"] + "-" + df_unpivoted['nama_ikan']
    df_unpivoted.info()
    return df_unpivoted

