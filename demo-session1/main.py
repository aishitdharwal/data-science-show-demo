import argparse

from src.tools.utils import (export_to_gsheet, load_yaml, process,
                             upload_df_to_s3)

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
config_export = config[args.task]["export"]

if config_export[0]["export"]["host"] == 's3':
    upload_df_to_s3(process(args.task), config_export[0]["export"]["prefix_filename"])
elif config_export[0]["export"]["host"] == 'gsheet':
    export_to_gsheet(config_export[0]["export"]["spreadsheet_id"], process(args.task), 
                     config_export[0]["export"]["clear_sheet"])
        

        