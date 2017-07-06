# coding=utf-8
#!/usr/bin/env python

import click

import pandas as pd
import optparse
from yaml import load, dump
import sys

# TODO: data validation at the end
# TODO: add logging
# TODO: add tests

def get_mapping_fields():
    try:
        with open('join_fields.yml', 'rb') as csv_file:
            data = load(csv_file)
            return data
    except:
        sys.exit('It needs a file join_fields.yml with the fields for the join.')

@click.command()
@click.option('--payments_filename', default='etl_data/01-openpayments_physicians.csv', help='Open payments providers file name.')
@click.option('--nppes_filename', default='etl_data/02-nppes_npi.csv', help='NPI providers file name.')
@click.option('--out', default='etl_data/openpayments_physicians_with_npi.csv', help='New file merging providers with its NPIs.')
def merge_files(payments_filename, nppes_filename, out):
    """It reads both CSV files and merge them into a new one."""

    # The files to merge.
    payments = pd.read_csv(payments_filename)
    nppes = pd.read_csv(nppes_filename)

    merged = merge_physicians(payments, nppes)

    # Save to the new CSV file.
    merged.to_csv(out, index=False)

    click.echo('Created new file %s!' % out)

    # Check that all the rows in payments are included and have NPI    

def merge_physicians(payments, nppes):
    """Creates a dataframe that has all the information from the Open Payments provider table, plus each provider's NPI."""

    # The fields to do the join between files.
    fields_to_map = get_mapping_fields()

    # Because pandas merge use sensitive case we need to lower the case for both.
    for key in fields_to_map:
        nppes[key] = nppes[key].str.lower()
        payments[fields_to_map[key]] = payments[fields_to_map[key]].str.lower()
    
    # Confirm that our fields to map are indexes of the CSV tables.
    try:
        payments.set_index(fields_to_map.values(), verify_integrity=True)
    except:
        sys.exit('There are duplicate rows for those keys in the map.')

    # Left Join on the payments file with the file that has the NPI by the physician name.
    full_merged = pd.merge(payments, nppes, how='left', left_on=fields_to_map.values(), right_on=fields_to_map.keys(), indicator=True)
    
    # Only get the columns that I want to save back.
    new_columns = list(payments.columns.values)
    new_columns.append('NPI')

    merged = full_merged.ix[:, new_columns]

    return merged


if __name__ == '__main__':
    merge_files()