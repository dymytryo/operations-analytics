-- One-time conversion: materialize the curated table as Parquet (SNAPPY),
-- decoupling it from the seed CSV in S3. From here on, the external seed
-- table can be dropped; all writes go to this table.

CREATE TABLE IF NOT EXISTS lake.ops_merchant_contact_info
WITH (
    format              = 'Parquet',
    parquet_compression = 'SNAPPY'
) AS
SELECT
    *
FROM
    lake.ops_merchant_contact_seed;
