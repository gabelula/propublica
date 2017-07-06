# README

[![goodtables.io](https://goodtables.io/badge/github/gabelula/propublica.svg)](https://goodtables.io/github/gabelula/propublica)

Merge two CSV files based on a YML mapping file. 

## Install

Clone this repository

```git clone git@github.com:gabelula/propublica.git```

Install requirements

```pip install -r requirements.txt```

## Usage

For this script to works it needs a file 'join_fields.yml' that defines which columns it will do the LEFT JOIN on. Copy the file 'join_fields.yml.sample' into 'join_fields.yml'.

```
Usage: merge.py [OPTIONS]

  Script that creates a CSV that has all the information from the Open
  Payments provider table, plus each provider's NPI.

Options:
  --payments_filename TEXT  Open payments providers file name.
  --nppes_filename TEXT     NPI providers file name.
  --out TEXT                New file merging providers with its NPIs.
  --help                    Show this message and exit.
```

## Glossary

#### National Provider Identifier (NPI)

A National Provider Identifier or NPI is a unique 10-digit identification number issued to health care providers in the United States by the Centers for Medicare and Medicaid Services (CMS). [Wikipedia](https://en.wikipedia.org/wiki/National_Provider_Identifier)

