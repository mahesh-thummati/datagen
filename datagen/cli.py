import argparse
import logging
import os
import random
import sys
import time
import pandas as pd

from datagen import VERSION
from datagen.fake_helper import FakeHelper
from datagen.io_helper import IOHelper
from datagen import config_parser

__author__ = 'mthummati'

def generate_fake_df(schema_parsed):
    faker = FakeHelper(schema_parsed.names.output_rec_cnt)
    output_df = pd.DataFrame()
    for field in schema_parsed.fields:
        start_time = time.time() #degug
        name = field.name
        (status, field_list) = faker.fake_it(field.type, field.min_length, 
            field.max_length, field.min_value, field.max_value, field.format, field.values)
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
            print ("Time taken to persist data: {0} seconds".format(end_time - start_time)) #degug
            print ("All set! data has been successfully persisted as parquet!")
    else:
        kwargs = dict(header=True, index=False, sep="|")
        status = iohelp.write_as_csv(output_df, schema_parsed.names.output_file, **kwargs)
        if status:
            end_time = time.time() #degug
            print ("Time taken to persist DF: {0} seconds".format(end_time - start_time)) #degug
            print ("All set! data has been successfully persisted as csv!")

def parse_json_config(input_schema):
    start_time = time.time() #degug
    schema_parsed = config_parser.parse(input_schema)
    end_time = time.time() #degug
    print ("Time taken to parse schema: {0} seconds".format(end_time - start_time)) #degug
    return schema_parsed

class Command:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
    
    def execute(self):
        """
        Given the command-line arguments, this creates a parser appropriate
        to that command, and runs it.
        """
        here = os.path.normpath(os.path.abspath(os.path.dirname(__file__)) + os.sep + os.pardir)
        with open(os.path.join(here, 'README.rst'), encoding='utf-8') as fp:
            README = fp.read()
        epilog = README
        formatter_class = argparse.RawDescriptionHelpFormatter
        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description='{} version {}'.format(self.prog_name, VERSION),
            epilog=epilog,
            formatter_class=formatter_class)
        
        group = parser.add_mutually_exclusive_group()
        group.add_argument("-v", "--verbose", action="store_true")
        group.add_argument("-q", "--quiet", action="store_true")
        
        parser.add_argument("action",
            metavar="action",
            choices=['execute', 'validate'],
            help="action to execute")

        parser.add_argument("inp_json",
            metavar="inp_json",
            help="input json file")
        
        arguments = parser.parse_args(self.argv[1:])

        if arguments.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.CRITICAL)

        if arguments.action == "execute":
            schema_parsed = parse_json_config(arguments.inp_json)
            if schema_parsed.names.source == "fake":
                output_df = generate_fake_df(schema_parsed)
                persist_df (schema_parsed, output_df)
        elif arguments.action == "validate":
            schema_parsed = parse_json_config(arguments.inp_json)


def execute_from_command_line(argv=None):
    """A simple method that runs a Command."""
    command = Command(argv)
    command.execute()