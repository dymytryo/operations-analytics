-- One-time bootstrap: register the seed CSV (exported from the notebook)
-- as an external table so Athena can read the initial schema.
-- Runs once; idempotent via IF NOT EXISTS.

CREATE EXTERNAL TABLE IF NOT EXISTS lake.ops_merchant_contact_seed (
    last_contact_date            DATE,
    merchant_id                  STRING,
    rep_id                       STRING,
    payor_id                     STRING,
    contact_type                 INT,
    call_outcome                 INT,
    email_contact                INT,
    city_name                    STRING,
    state                        STRING,
    transaction_volume_lifetime  DOUBLE
)
-- LazySimpleSerDe handles the delimited seed file
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ',',
    'field.delim'          = ',',
    'collection.delim'     = '|',
    'mapkey.delim'         = ':',
    'escape.delim'         = '\\'
)
LOCATION 's3://company-datalake/ops/sheets_seed/'
TBLPROPERTIES (
    'classification'         = 'csv',
    'has_encrypted_data'     = 'false',
    'skip.header.line.count' = '1'
);
