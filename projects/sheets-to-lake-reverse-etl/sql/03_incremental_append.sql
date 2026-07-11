-- Daily append: insert only records not already present, keyed on
-- record identity + contact date, so a rerun of the pipeline cannot
-- double-count an outreach.
--
-- Hardening note: on an Iceberg table this becomes a MERGE, which also
-- covers late corrections from the ops sheet (updates, not just inserts).

INSERT INTO lake.ops_merchant_contact_info
SELECT
    s.last_contact_date,
    s.merchant_id,
    s.rep_id,
    s.payor_id,
    s.contact_type,
    s.call_outcome,
    s.email_contact,
    s.city_name,
    s.state,
    s.transaction_volume_lifetime
FROM
    lake.ops_merchant_contact_staging s
LEFT JOIN
    lake.ops_merchant_contact_info t
    ON  t.merchant_id       = s.merchant_id
    AND t.last_contact_date = s.last_contact_date
WHERE
    t.merchant_id IS NULL;
