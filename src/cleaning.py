"""Reusable cleaning functions for the GSAF shark-incident dataset."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with stripped, lowercase snake_case column names."""
    result = df.copy()
    result.columns = (
        result.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return result


def remove_empty_and_irrelevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully empty columns and reference fields not used in this analysis."""
    result = df.dropna(axis=1, how="all").copy()
    irrelevant = {
        "href_formula", "href", "pdf", "case_number", "case_number_1",
        "original_order", "source", "name",
    }
    return result.drop(columns=[c for c in irrelevant if c in result.columns])


def normalize_text(value: object) -> object:
    """Normalize whitespace while retaining missing values."""
    if pd.isna(value):
        return pd.NA
    text = unicodedata.normalize("NFKC", str(value))
    text = re.sub(r"\s+", " ", text).strip()
    return text if text else pd.NA


def clean_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize whitespace and capitalization in selected text fields."""
    result = df.copy()
    fields = ["type", "country", "state", "location", "activity", "injury", "species"]
    for column in fields:
        if column in result:
            result[column] = result[column].map(normalize_text)
    if "country" in result:
        result["country"] = result["country"].str.upper()
    if "type" in result:
        result["type"] = result["type"].str.title()
    return result


def clean_year_and_date(df: pd.DataFrame) -> pd.DataFrame:
    """Create valid numeric year and parsed date fields."""
    result = df.copy()
    result["year"] = pd.to_numeric(result["year"], errors="coerce").astype("Int64")
    result.loc[~result["year"].between(1500, 2026), "year"] = pd.NA

    # The source date often omits its year. Combine cleaned day/month text with year.
    date_text = result["date"].astype("string")
    date_text = date_text.str.replace(r"(?i)(\d+)(st|nd|rd|th)", r"\1", regex=True)
    date_text = date_text.str.replace(r"\s+", " ", regex=True).str.strip()
    combined = date_text + " " + result["year"].astype("string")
    result["incident_date"] = pd.to_datetime(combined, errors="coerce", dayfirst=True)
    result["month"] = result["incident_date"].dt.month_name()
    result["decade"] = (result["year"] // 10 * 10).astype("Int64")
    return result


def clean_sex(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize sex to M/F/Unknown."""
    result = df.copy()
    raw = result["sex"].astype("string").str.strip().str.upper()
    result["sex_clean"] = raw.map({"M": "M", "F": "F"}).fillna("Unknown")
    return result.drop(columns="sex")


def clean_age(df: pd.DataFrame) -> pd.DataFrame:
    """Extract the first plausible numeric age and create age bands."""
    result = df.copy()
    extracted = result["age"].astype("string").str.extract(r"(\d{1,3})", expand=False)
    result["age_numeric"] = pd.to_numeric(extracted, errors="coerce")
    result.loc[~result["age_numeric"].between(1, 100), "age_numeric"] = np.nan
    result["age_group"] = pd.cut(
        result["age_numeric"],
        bins=[0, 17, 29, 44, 59, 100],
        labels=["0–17", "18–29", "30–44", "45–59", "60+"],
    ).astype("string").fillna("Unknown")
    return result.drop(columns="age")


def clean_fatal_status(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize the fatal indicator without guessing ambiguous records."""
    result = df.copy()
    raw = result["fatal_y_n"].astype("string").str.strip().str.upper()
    result["fatal"] = np.select(
        [raw.str.match(r"^Y", na=False), raw.str.match(r"^N", na=False)],
        ["Yes", "No"],
        default="Unknown",
    )
    return result.drop(columns="fatal_y_n")


def group_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Group free-text activities into transparent regex-based categories."""
    result = df.copy()
    activity = result["activity"].astype("string")
    conditions = [
        activity.str.contains(r"surf|body.?board|boogie", case=False, na=False),
        activity.str.contains(r"swim|bathing|float|wading", case=False, na=False),
        activity.str.contains(r"fish|angl|spearfish", case=False, na=False),
        activity.str.contains(r"div|snorkel", case=False, na=False),
        activity.str.contains(r"kayak|canoe|paddle|rowing", case=False, na=False),
        activity.str.contains(r"boat|sail|yacht|ship", case=False, na=False),
    ]
    labels = ["Surfing", "Swimming/Wading", "Fishing", "Diving/Snorkeling", "Paddling", "Boating"]
    result["activity_group"] = np.select(conditions, labels, default="Other/Unknown")
    return result


def clean_type(df: pd.DataFrame) -> pd.DataFrame:
    """Consolidate incident types used for filtering."""
    result = df.copy()
    raw = result["type"].astype("string")
    result["incident_type"] = np.select(
        [
            raw.str.contains("Unprovoked", case=False, na=False),
            raw.str.contains("Provoked", case=False, na=False),
            raw.str.contains("Watercraft|Boat", case=False, na=False),
            raw.str.contains("Sea Disaster|Air", case=False, na=False),
            raw.str.contains("Questionable|Invalid", case=False, na=False),
        ],
        ["Unprovoked", "Provoked", "Watercraft", "Sea disaster", "Questionable"],
        default="Other/Unknown",
    )
    return result.drop(columns="type")


def clean_shark_data(df: pd.DataFrame) -> pd.DataFrame:
    """Run the complete, ordered cleaning pipeline."""
    result = standardize_columns(df)
    result = remove_empty_and_irrelevant_columns(result)
    result = result.drop_duplicates().reset_index(drop=True)
    result = clean_text_fields(result)
    result = clean_year_and_date(result)
    result = clean_sex(result)
    result = clean_age(result)
    result = clean_fatal_status(result)
    result = group_activity(result)
    result = clean_type(result)
    return result


def load_and_clean(path: str | Path) -> pd.DataFrame:
    """Load the official GSAF Excel file and return the cleaned table."""
    raw = pd.read_excel(path, sheet_name="Sheet1-GSAF")
    return clean_shark_data(raw)

