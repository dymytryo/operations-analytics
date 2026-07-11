"""Google Sheets read/write helpers for the ops enrichment pipeline.

Sanitized from production: sheet IDs, ranges, and the OAuth client secret
are placeholders. The token cache pattern keeps daily scheduled runs
non-interactive after a one-time consent.
"""

import logging
import pickle
from pathlib import Path

import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CLIENT_SECRET_FILE = "client_secret.json"   # never committed
TOKEN_CACHE = Path("token.pickle")          # never committed


def get_credentials():
    """Return valid OAuth credentials, refreshing or prompting as needed."""
    creds = None
    if TOKEN_CACHE.exists():
        with TOKEN_CACHE.open("rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with TOKEN_CACHE.open("wb") as token:
            pickle.dump(creds, token)

    return creds


def sheet_id_from_url(url: str) -> str:
    """Extract the spreadsheet id from a full Sheets URL."""
    return url.split("/")[5]


def read_sheet(sheet_id: str, sheet_range: str) -> pd.DataFrame:
    """Read a range into a DataFrame, promoting the first row to header."""
    creds = get_credentials()
    try:
        service = build("sheets", "v4", credentials=creds)
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=sheet_id, range=sheet_range)
            .execute()
        )
        values = result.get("values", [])
    except HttpError:
        logger.exception("Sheets API read failed for range %s", sheet_range)
        raise

    if not values:
        logger.warning("No data found in range %s", sheet_range)
        return pd.DataFrame()

    df = pd.DataFrame(values[1:], columns=values[0])
    return df


def write_sheet(sheet_id: str, sheet_range: str, df: pd.DataFrame) -> None:
    """Replace a range with the DataFrame's values (clear, then append).

    Production note: prefer a named range over hard coordinates so a column
    inserted by the ops team cannot silently shift the write target.
    """
    creds = get_credentials()
    body = {"majorDimension": "ROWS", "values": df.values.tolist()}
    try:
        service = build("sheets", "v4", credentials=creds)
        sheets = service.spreadsheets().values()
        sheets.clear(spreadsheetId=sheet_id, range=sheet_range).execute()
        sheets.append(
            spreadsheetId=sheet_id,
            range=sheet_range,
            body=body,
            valueInputOption="USER_ENTERED",
        ).execute()
    except HttpError:
        logger.exception("Sheets API write failed for range %s", sheet_range)
        raise
