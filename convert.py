#!/usr/bin/env python3

import sys
import os.path
import re
import pandas as pd
import numpy as np
import time
import datetime


script = sys.argv[0]

if len(sys.argv) != 4 :
	print ("Usage: ", script, " <excel_file> <sheet_name> <schema_file>")
	sys.exit("Expecting 3 arguments.")

excel_file = sys.argv[1]
sheet_name = sys.argv[2]
schema_file = sys.argv[3]


def parse_schema(schema_file):
	if os.path.exists(schema_file) == False:
		error_msg = "ERROR: Schema file not found: {}".format(schema_file)
		sys.exit(error_msg)

	columns = []
	with open(schema_file, 'r') as myfile:
		data = myfile.read().replace('\r\n', '').replace('\n', '').lower()
		data = re.sub('comment [^,]+,', ',', data)

		result = re.search("create table .*\((.*)\)", data)
		result = result.group(1)

		columns = result.split(",")
		columns = [x.strip() for x in columns]

		columns = [tuple(x.split(' ')) for x in columns]

	return [x[0] for x in columns], [x[1] for x in columns]


def read_excel(excel_file, sheet_name):
	if os.path.exists(excel_file) == False:
		error_msg = "ERROR: Excel file not found: {}".format(excel_file)
		sys.exit(error_msg)

	print ()
	print ("Reading excel...")
	print ("FILE:", excel_file)
	start_time = time.time()

	# Read excel file
	xl = pd.ExcelFile(excel_file)
	df = xl.parse(sheet_name)

	time_taken = str(datetime.timedelta(seconds=(time.time() - start_time)))
	print("Read excel in %s." % time_taken)
	print ()

	return df


def write_parquet(df):
	print ()
	print ("Writing parquet file...")
	start_time = time.time()
	print ("FILE:", sheet_name)
	# Write out a parquet file.
	df.to_parquet(sheet_name + '.parq', compression=None)
	
	time_taken = str(datetime.timedelta(seconds=(time.time() - start_time)))
	print("Wrote parquet file in %s." % time_taken)
	print()


if __name__ == "__main__":

	df = read_excel(excel_file, sheet_name)
	
	print ("Excel sheet has", len(df.columns.values), "columns.")
	print ("EXCEL COLUMNS:")
	print (df.columns.values)
	
	col_names, col_types = parse_schema(schema_file)

	num_columns_to_load = len(col_names)

	print()
	print ("Only loading first", num_columns_to_load, "columns.")
	print ()

	# Keep only the first n columns from excel sheet
	df = df.iloc[:,0:num_columns_to_load]

	# Rename dataframe column header
	print ("OLD HEADER: ")
	print (list(df.columns.values))
	print ()
	print ("NEW HEADER: ")
	print (col_names)
	print()

	df.columns = col_names

	write_parquet(df)
