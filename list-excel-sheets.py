#!/usr/bin/env python3

import sys
import os.path
import pandas as pd

script=sys.argv[0]

if len(sys.argv) != 2 :
	print("Usage: ", script, " <path_to_excel_file>")
	sys.exit("Expecting argument.")

excel_file_path=sys.argv[1]

if os.path.exists(excel_file_path) == False:
	print("ERROR: ", excel_file_path, " doesn't exist.")
	sys.exit("Excel file not found.")

xl = pd.ExcelFile(excel_file_path)

print(xl.sheet_names)

