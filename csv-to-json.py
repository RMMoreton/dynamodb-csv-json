"""Convert a dynamoDB exported CSV into JSON.

The output file will be uploadable to Dynamo via
`aws dynamodb batch-write-item --request-items file://<output-name>`.
"""


import argparse
import json


def parse_args():
    """Read the file name, table name, and optional output name."""
    parser = argparse.ArgumentParser(description='Parse a dynamodb'
                                     ' csv file into json.')
    parser.add_argument('file_name',
                        help='The name of your file')
    parser.add_argument('table_name',
                        help='The name of the table to import to')
    parser.add_argument('--output_name',
                        help='The name of the output file.')
    args = parser.parse_args()
    return args


def get_output_name(args):
    """Get the name of the file to output to."""
    output_name = args.output_name
    if output_name is not None:
        return output_name
    input_name = args.file_name
    base = input_name.rsplit('.', 1)[0]
    return '{}.json'.format(base)


def get_format(f):
    """Read the format line from the top of the CSV."""
    format = f.readline().strip()
    fields = format.split(',')
    field_tuples = []
    for field in fields:
        field = field.strip('"')
        name, t = field.split(' ')
        t = t.strip('()')
        field_tuples.append((name, t))
    return field_tuples


def create_requests(f, field_tuples):
    """Create a list of PutItem requests."""
    requests = []
    for line in f:
        item = {}
        values = line.strip().split(',')
        for i, value in enumerate(values):
            field = field_tuples[i]
            name = field[0]
            t = field[1]
            value = value.strip('"')
            item[name] = {t: value}
        requests.append(create_put_request(item))
    return requests


def create_put_request(item):
    """Create a PutRequest object."""
    return {'PutRequest': {'Item': item}}


def create_full_request(requests, table_name):
    """Create the request items object."""
    return {table_name: requests}


def write_to_file(full_request, file_name):
    """Write the request object."""
    with open(file_name, 'w') as w:
        json.dump(full_request, w)


def main():
    """Run the program."""
    args = parse_args()
    file_name = args.file_name
    out_file_name = get_output_name(args)
    with open(file_name, 'r') as f:
        field_tuples = get_format(f)
        requests = create_requests(f, field_tuples)
    full_request = create_full_request(requests, args.table_name)
    write_to_file(full_request, out_file_name)


if __name__ == '__main__':
    main()
