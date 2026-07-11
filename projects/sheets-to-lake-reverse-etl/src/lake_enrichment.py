"""Batched Athena lookups that enrich ops records with lake context.

Query shapes are sanitized; the batching and merge mechanics are the
production pattern.
"""

import logging
from functools import reduce
from typing import Iterable, Sequence

import pandas as pd
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

logger = logging.getLogger(__name__)

S3_STAGING_DIR = "s3://company-athena-results/"   # placeholder
REGION = "us-east-1"
WORK_GROUP = "Analyst"

# Athena bounds query string size; keep IN-lists comfortably under it.
BATCH_SIZE = 1_000

MERCHANT_TRANSACTIONS_QUERY = """
    SELECT
        record_id,
        merchant_id,
        COUNT(*)            AS transactions_last_month,
        SUM(amount_usd)     AS volume_last_month_usd
    FROM
        lake.merchant_transactions
    WHERE
        TRUE
        AND transaction_month = DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1' MONTH)
        AND merchant_id IN ({placeholders})
    GROUP BY
        1, 2
"""


def athena_cursor():
    """Open a PandasCursor against the analyst work group."""
    return connect(
        s3_staging_dir=S3_STAGING_DIR,
        region_name=REGION,
        work_group=WORK_GROUP,
        cursor_class=PandasCursor,
    ).cursor()


def batched(keys: Sequence[str], size: int = BATCH_SIZE) -> Iterable[Sequence[str]]:
    """Yield key chunks small enough to interpolate into an IN clause."""
    for start in range(0, len(keys), size):
        yield keys[start : start + size]


def fetch_merchant_context(merchant_ids: Sequence[str]) -> pd.DataFrame:
    """Run the lookup query per batch and concatenate the results."""
    frames = []
    cursor = athena_cursor()
    try:
        for chunk in batched(list(merchant_ids)):
            placeholders = ", ".join(f"'{m}'" for m in chunk)
            query = MERCHANT_TRANSACTIONS_QUERY.format(placeholders=placeholders)
            frames.append(cursor.execute(query).as_pandas())
    finally:
        cursor.close()

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def merge_context(base: pd.DataFrame, lookups: list[pd.DataFrame]) -> pd.DataFrame:
    """Merge every lookup result onto the base frame by record_id."""
    frames = [base] + [f for f in lookups if not f.empty]
    return reduce(
        lambda left, right: pd.merge(left, right, on=["record_id"], how="left"),
        frames,
    )
