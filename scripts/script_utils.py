import json
import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen


def is_up_to_date(output_filename, urls):
    try:
        with open(output_filename) as f:
            # file exists, check if URLs have changed
            gj = json.load(f)
            data_source_urls = gj['metadata']['data_source_urls']
            if any(k not in data_source_urls for k in urls):
                print(f"{output_filename} exists but URLs have changed, will recreate")
                return False
            print(f"{output_filename} is up to date, skipping")
            return True
    except:
        print(f"Creating {output_filename}")
        return False


def load_dataframe(urls, db_name, sheet_name=0, skiprows=None):
    '''
    Return a dataframe for the given urls, database name and sheet name.
    '''
    if db_name + "_csv" in urls:
        return pd.read_csv(urls[db_name + "_csv"], skiprows=skiprows)
    elif db_name + "_xlsx" in urls:
        return pd.read_excel(urls[db_name + "_xlsx"], sheet_name=sheet_name, skiprows=skiprows)
    elif db_name + "_xlsm" in urls:
        with urlopen(urls[db_name + "_xlsm"]) as xlsm_file:
            return pd.read_excel(BytesIO(xlsm_file.read()), sheet_name=sheet_name, skiprows=skiprows)
    elif db_name + "_zip" in urls:
        with urlopen(urls[db_name + "_zip"]) as zip_file:
            with ZipFile(BytesIO(zip_file.read())) as zip_ref:
                with zip_ref.open(zip_ref.namelist()[0]) as xlsm_file:
                    return pd.read_excel(xlsm_file, sheet_name=sheet_name, skiprows=skiprows)
