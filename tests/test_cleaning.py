import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cleaning import clean_shark_data


def test_cleaning_pipeline_standardizes_key_fields():
    raw = pd.DataFrame(
        {
            "Date": ["3rd June", "3rd June"],
            "Year": [2020, 2020],
            "Type": [" Unprovoked ", " Unprovoked "],
            "Country": [" usa ", " usa "],
            "State": ["Florida", "Florida"],
            "Location": ["Beach", "Beach"],
            "Activity": ["Board surfing", "Board surfing"],
            "Sex": ["m", "m"],
            "Age": ["About 24 years", "About 24 years"],
            "Injury": ["Minor", "Minor"],
            "Fatal Y/N": ["n", "n"],
            "Time": ["14:00", "14:00"],
            "Species ": ["Unknown", "Unknown"],
        }
    )
    cleaned = clean_shark_data(raw)
    assert len(cleaned) == 1
    assert cleaned.loc[0, "country"] == "USA"
    assert cleaned.loc[0, "age_numeric"] == 24
    assert cleaned.loc[0, "fatal"] == "No"
    assert cleaned.loc[0, "activity_group"] == "Surfing"
    assert cleaned.loc[0, "incident_type"] == "Unprovoked"

