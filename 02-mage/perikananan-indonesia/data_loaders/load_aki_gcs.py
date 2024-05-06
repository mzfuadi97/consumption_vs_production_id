from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

import pyarrow as pa
import pyarrow.parquet as pq
import os

schema = pa.schema([
    ('jenis_usaha', pa.string()),
    ('provinsi', pa.string()),
    ('jenis_ikan', pa.string()),
    ('tahun', pa.string()),
    ('volume_produksi', pa.int64()),
    ('nilai_produksi', pa.int64()),
    ('id', pa.string()),
    ('id_ikan', pa.string()),
    ("angka_konsumsi_ikan",pa.int64()),
    ("harga_ikan",pa.float32())
])

os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/home/src/keys.json'


project_id = 'secret-meridian-414302'
bucket_name = 'perikanan_indo_bucket_secret-meridian-414302'
table_name = 'perikanan_indo'

root_path = f'{bucket_name}/{table_name}' 

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    
    gcs = pa.fs.GcsFileSystem()

    dataset = pq.ParquetDataset(root_path, filesystem=gcs, schema = schema)

    data = dataset.read_pandas().to_pandas()

    return data
