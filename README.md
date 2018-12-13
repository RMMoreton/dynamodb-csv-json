# Dynamo CSV

## Convert a DynamoDB-exported CSV file to a DynamoDB-importable JSON file.

DynamoDB allows you to export items to CSV, but as far as I can tell it doesn't
allow you to upload those CSV files back in. I wrote this script to fix that.

## Usage

`python csv-to-json.py <input-file> <dynamo-table-name> [--output_name <name>]`

If you don't specify an output name, the script will strip the `.csv` from
your input file and output the JSON to `<base-file-name>.json`.