# Dynamo CSV

## Why?

DynamoDB allows you to export items to CSV, but as far as I can tell it doesn't
allow you to upload those CSV files back in. I wrote this script to fix that.

## Usage

`python csv-to-json.py <input-file> <dynamo-table-name> [--output_name <name>]`

If you don't specify an output name, the script will strip the `.csv` from
your input file and output the JSON to `<base-file-name>.json`.

## Caveats

This script doesn't use `boto3` to automatically upload your items for you,
although it could be modified to do that. You have to manually use the
`aws dynamodb batch-write-item --request-items file://<output-file>`
command.

The `aws dynamodb batch-write-item` command only accepts 25 items at most.
So if you export more than 25 items, convert them with this tool, and then
try and upload them you'll get an error. This could be fixed, but it isn't.