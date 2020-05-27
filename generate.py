import pandas as pd
import time

from datagen.fake_helper import FakeHelper
from datagen.io_helper import IOHelper
from datagen import config_parser


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

def generate_fake_df(schema_parsed):
    faker = FakeHelper(schema_parsed.names.output_rec_cnt)
    output_df = pd.DataFrame()
    for field in schema_parsed.fields:
        start_time = time.time() #degug
        name = field.name
        (status, field_list) = faker.fake_it(field.type, field.min_length, 
            field.max_length, field.min_value, field.max_value, field.values)
        if status:
            output_df[name] = field_list
        end_time = time.time() #degug
        print ("Time taken to generate {0}: {1} seconds".format(name, end_time - start_time)) #degug
    return output_df

def persist_df(schema_parsed, output_df):
    start_time = time.time() #degug
    iohelp = IOHelper("codecommit")
    if schema_parsed.names.output_format == "parquet":
        status = iohelp.write_as_parquet(output_df, schema_parsed.names.output_file)
        if status:
            end_time = time.time() #degug
            print ("Time taken to persist DF: {0} seconds".format(end_time - start_time)) #degug
            print ("pandas df has been successfully persisted as parquet!")
    else:
        kwargs = dict(header=True, index=False, sep="|")
        status = iohelp.write_as_csv(output_df, schema_parsed.names.output_file, **kwargs)
        if status:
            end_time = time.time() #degug
            print ("Time taken to persist DF: {0} seconds".format(end_time - start_time)) #degug
            print ("pandas df has been successfully persisted as csv!")

def parse_json_config(input_schema):
    start_time = time.time() #degug
    schema_parsed = config_parser.parse(input_schema)
    end_time = time.time() #degug
    print ("Time taken to parse schema: {0} seconds".format(end_time - start_time)) #degug

def main():
    """main method"""
    schema_parsed = parse_json_config(input_schema)
    if schema_parsed.names.source == "fake":
        output_df = generate_fake_df(schema_parsed)
        persist_df (schema_parsed, output_df)

if __name__ == "__main__":
    input_schema = "config.json"
    main()

    