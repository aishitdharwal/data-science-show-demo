import os
import argparse
import importlib
import pandas as pd
from src.tools.utils import import_from_s3, upload_df_to_s3, check_all_files_s3, load_yaml
from src.tools.import_data import process


#df = pd.read_csv("data/sales.csv",index_col=0)
#upload_df_to_s3(df, filename_prefix="processed_sales_")
#files = check_all_files_s3()
#df_read = import_from_s3(files[0])

args = argparse.ArgumentParser(
    description="Provies some inforamtion on the job to process"
)
args.add_argument(
    "-t",
    "--task",
    type=str,
    required=True,
    help="This will point to a task location into the config.yaml file.\
        Then it will follow the step of this specific task.")
args = args.parse_args()

config = load_yaml("./config/config.yaml")
args_task='testing'
#config[args_task]

config_export = config[args.task]["export"]

if config_export[0]["export"]["host"] == 's3':
    upload_df_to_s3(process(args_task), config_export[0]["export"]["prefix_filename"])