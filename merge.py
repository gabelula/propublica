# coding=utf-8
#!/usr/bin/env python

# Script that creates a CSV that has all the information from the Open Payments provider table, plus each provider's NPI.

import pandas as pd
import optparse
from yaml import load, dump

# TODO: data validation at the end

# TODO: manage errors
# TODO: convert it into a cli
# TODO: add logging
# TODO: add tests

def get_mapping_fields():
    with open('map.yml', 'rb') as csv_file:
        data = load(csv_file)
        return data

def main():
    
    # Get the options from the command line.
    p = optparse.OptionParser()
    p.add_option('--payments', '-p', default='etl_data/01-openpayments_physicians.csv')
    p.add_option('--out', '-o', default='etl_data/openpayments_physicians_with_npi.csv')
    p.add_option('--nppes', '-n', default='etl_data/02-nppes_npi.csv')

    options, arguments = p.parse_args()

    payments_file = options.payments
    new_payments_file = options.out
    nppes_file = options.nppes


    # The fields to do the join between files.
    fields_to_map = get_mapping_fields()

    # The files to merge.
    payments = pd.read_csv(payments_file)
    nppes = pd.read_csv(nppes_file)#, usecols=fields_to_map.keys)

    # Because pandas merge use sensitive case we need to lower the case for both.
    for key in fields_to_map:
        nppes[key] = nppes[key].str.lower()
        payments[fields_to_map[key]] = payments[fields_to_map[key]].str.lower()
    
    # Confirm that our fields to map are indexes of the CSV tables.

    # Left Join on the payments file with the file that has the NPI by the physician name.
    full_merged = pd.merge(payments, nppes, how='left', left_on=fields_to_map.values(), right_on=fields_to_map.keys(), indicator=True)
    
    # Only get the columns that I want to save back.
    new_columns = list(payments.columns.values)
    new_columns.append('NPI')

    merged = full_merged.ix[:, new_columns]

    # Save to the new CSV file.
    merged.to_csv(new_payments_file, index=False)

if __name__ == '__main__':
    main()