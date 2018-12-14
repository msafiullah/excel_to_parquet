#!/usr/bin/env python3

import sys
import os.path
import pyarrow.parquet as pq

parquet_file_path=sys.argv[0]

script=sys.argv[0]

if len(sys.argv) != 2 :
	print("Usage: ", script, " <path_to_parquet_file>")
	sys.exit("Expecting argument.")

parquet_file_path=sys.argv[1]

if os.path.exists(parquet_file_path) == False:
	print("ERROR: ", parquet_file_path, " doesn't exist.")
	sys.exit("Parquet file not found.")

parquet_file = pq.ParquetFile(parquet_file_path)
print ( parquet_file.metadata.num_rows )

