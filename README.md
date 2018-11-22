# excel_to_parquet
Convert excel to parquet for quick loading into Hive table.

### Install Python Packages ###
```
pip3 install --user -r requirements.txt
```

### Run ###
```
python3 convert.py sample.xlsx Sheet1 schema.hql
```

### Upload parquet file to HDFS ###
```
hdfs dfs -put Sheet1.parq /path/to/folder/in/hdfs
```

### Load to table ###
Execute the following in Beeline.
```
USE database_name;

-- Create table
!run /path/to/where/you/stored/schema.hql

-- Load data into table
LOAD DATA INPATH '/path/in/hdfs/to/parquet/Sheet1.parq' INTO TABLE sample_table; 


-- Original table's parquet format is incompatible with hive.
-- So, create new table in Hive as parquet to store a copy of original table.
DROP TABLE IF EXISTS tmp_sample_table; 
CREATE TABLE tmp_sample_table STORED AS PARQUET AS SELECT * FROM sample_table; 

DROP TABLE sample_table; 
ALTER TABLE tmp_sample_table RENAME TO sample_table;
```
