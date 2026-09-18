# SharkSafe: Cleaning and Exploring Global Shark Incidents

An Ironhack data-wrangling mini-project using Python and pandas to transform the messy Global Shark Attack File (GSAF) incident log into analysis-ready data.

## Project question

**Which activities and locations appear most frequently in recorded unprovoked shark incidents from 2000 through 2025, and how do fatal outcomes differ across activity groups?**

### Hypothesis

Surfing will be the most frequently recorded activity among modern unprovoked shark incidents.

This project analyses *incident counts*, not true risk. The dataset does not contain the number of people exposed to each activity or location, so it cannot establish that one activity or country is inherently more dangerous.

## Dataset

- Source: [Global Shark Attack File incident log](https://www.sharkattackfile.net/incidentlog.htm)
- Download used: `GSAF5.xls`
- Raw observations: **7,117**
- Historical coverage: records extending from early historical cases through 2026
- Analysis window: **2000–2025**, excluding the incomplete 2026 year
- Analysis population: records classified as **Unprovoked** by GSAF

The source is continually updated, so rerunning the project with a later download may produce different totals.

## Cleaning performed

The reusable pipeline in `src/cleaning.py` performs the following operations:

1. Standardizes column names to `snake_case`.
2. Removes fully empty and analysis-irrelevant columns.
3. Removes exact duplicate rows.
4. Normalizes Unicode, whitespace, capitalization, and country names.
5. Converts year values to a nullable numeric type and filters implausible years.
6. Removes ordinal suffixes and parses incident dates.
7. Standardizes sex and fatal-status categories without guessing ambiguous values.
8. Uses regular expressions to extract plausible numeric ages.
9. Creates age groups, months, and decades.
10. Uses transparent regex rules to consolidate free-text activities.
11. Consolidates source incident types for consistent filtering.

## Principal findings

For unprovoked incidents from 2000 through 2025:

- The analysis contains **2,220** records.
- **Surfing** is the most frequently recorded activity group, with **966** incidents.
- The **USA** has the most recorded incidents, with **1,125**.
- Fatal status is known for **2,203** records.
- **10.80%** of records with known outcomes are fatal.

The activity result supports the hypothesis within the chosen analytical scope. It must not be interpreted as proof that surfing has the greatest individual risk, because participation and exposure totals are unavailable.

## Repository structure

```text
data-cleaning-pandas/
├── data/
│   ├── raw/GSAF5.xls
│   └── cleaned/shark_attacks_clean.csv
├── notebooks/shark_attacks_analysis.ipynb
├── outputs/
│   ├── 01_activity_counts.png
│   ├── 02_top_countries.png
│   ├── 03_fatal_by_activity.png
│   ├── 04_incidents_over_time.png
│   └── supporting CSV tables
├── src/
│   ├── cleaning.py
│   └── analysis.py
├── tests/test_cleaning.py
├── PRESENTATION.md
├── requirements.txt
└── README.md
```

## How to run

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Run the complete pipeline:

```bash
python src/analysis.py
```

Or open and run:

```text
notebooks/shark_attacks_analysis.ipynb
```

## Limitations

- This is a record of reported incidents, not all human exposure to oceans.
- Reporting completeness varies by country and historical period.
- Activity and species fields are free text and require subjective grouping rules.
- Missing and ambiguous values are retained as unknown rather than guessed.
- Fatality percentages are calculated only where fatal status is known.
- The analysis excludes incomplete 2026 data to avoid comparing a partial year with full years.

## Presentation

The complete 5-minute slide script and demo plan are in [`PRESENTATION.md`](PRESENTATION.md). Before submission, transfer the slides to Google Slides, Slides.com, or Prezi and place the public URL here.

**Online presentation URL:** `[ADD ONLINE SLIDE LINK]`

## Authors

Paul Omogiate Obamwonyi and project team.

