"""The daily enrichment run, end to end.

Triggered by an EventBridge cron that starts the SageMaker notebook job.
Each stage logs failures with full context so a missed run is diagnosable
from CloudWatch alone.
"""

import logging

import lake_enrichment
import sheets_client

logger = logging.getLogger(__name__)

SHEET_URL = "https://docs.google.com/spreadsheets/d/EXAMPLE_SHEET_ID/edit"
WORKING_RANGE = "Operations Support Campaign"
WRITEBACK_RANGE = "Operations Support Campaign!EnrichedColumns"  # named range

ATHENA_TABLE = "lake.ops_merchant_contact_info"


def run() -> None:
    sheet_id = sheets_client.sheet_id_from_url(SHEET_URL)

    # 1. Extract the ops team's working sheet.
    records = sheets_client.read_sheet(sheet_id, WORKING_RANGE)
    if records.empty:
        logger.warning("Sheet returned no records; nothing to do.")
        return

    # 2. Enrich only the rows that are missing lake context.
    needs_context = records[records["transactions last month"].isna()]
    context = lake_enrichment.fetch_merchant_context(
        needs_context["merchant id"].tolist()
    )
    enriched = lake_enrichment.merge_context(records, [context])

    # 3. Write the enriched columns back for the ops team.
    sheets_client.write_sheet(sheet_id, WRITEBACK_RANGE, enriched)

    # 4. Append the curated records to the Parquet table (sql/03).
    #    Appends are keyed on record_id + contact date, so reruns are safe.
    cursor = lake_enrichment.athena_cursor()
    try:
        insert_sql = open("sql/03_incremental_append.sql").read()
        cursor.execute(insert_sql)
    finally:
        cursor.close()

    logger.info("Enriched %s records; appended to %s.", len(enriched), ATHENA_TABLE)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()
