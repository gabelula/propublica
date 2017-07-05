# coding=utf-8
#!/usr/bin/env python

# Script that creates a CSV that has all the information from the Open Payments provider table, plus each provider's NPI.

import csv
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

# Look for the NPI field by fields and its values. 
def search_npi(file, npi_field, fields):
    
    with open(file, 'rb') as csv_file:
        npis = csv.DictReader(csv_file)
        for row in npis:
            temp = filter(lambda x: row[x] == fields[x], fields)
            if temp and reduce(lambda x, y: x and y, temp):
                return row[npi_field]
    
    return null


def get_values_to_identify_physician(row):

    fields = {}    
    map = get_mapping_fields()

    for k in map['fields']:
        fields[map['fields'][k]] = row[k]

    return fields


def process_rows(payments, nppes_file):
    rows = []
    for row in payments:
        fields = get_values_to_identify_physician(row)
        row['NPI'] = search_npi(nppes_file, 'NPI', fields)
        rows.append(row)
    return rows

def main():
    p = optparse.OptionParser()
    p.add_option('--payments', '-p', default='etl_data/01-openpayments_physicians.csv')
    p.add_option('--out', '-o', default='etl_data/openpayments_physicians_with_npi.csv')
    p.add_option('--nppes', '-n', default='etl_data/02-nppes_npi.csv')

    options, arguments = p.parse_args()

    payments_file = options.payments
    new_payments_file = options.out
    nppes_file = options.nppes

    with open(payments_file, 'rb') as csv_file:
        payments = csv.DictReader(csv_file)
        
        new_fieldnames = payments.fieldnames
        new_fieldnames.append('NPI')

        with open(new_payments_file, 'wb') as new_csv_file:
            payments_with_npi = csv.DictWriter(new_csv_file, fieldnames=new_fieldnames)
            payments_with_npi.writeheader()
            new_rows = process_rows(payments, nppes_file)
            payments_with_npi.writerows(new_rows)
            

if __name__ == '__main__':
    main()