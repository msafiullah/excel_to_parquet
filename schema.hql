DROP TABLE IF EXISTS sample_table;

CREATE TABLE IF NOT EXISTS sample_table
(
id double COMMENT "hahaha",
name string,
dob string
)
STORED AS PARQUET
;
