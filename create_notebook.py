import json
from pathlib import Path


def markdown(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source):
    return {
        "cell_type": "code", "execution_count": None, "metadata": {},
        "outputs": [], "source": source.splitlines(keepends=True),
    }


root = Path(__file__).resolve().parent
nb = {
    "cells": [],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

cells = []
cells.append(markdown("""# SharkSafe: Data Wrangling and EDA

**Question:** Which activities and locations appear most frequently in recorded unprovoked shark incidents from 2000–2025, and how do fatal outcomes differ across activity groups?

**Hypothesis:** Surfing will be the most frequently recorded activity.

> This analysis describes reported incidents, not actual risk. Exposure totals are unavailable."""))
cells.append(code("""from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cleaning import clean_shark_data

sns.set_theme(style='whitegrid')
RAW_PATH = ROOT / 'data' / 'raw' / 'GSAF5.xls'"""))
cells.append(markdown("## 1. Load and inspect the raw data"))
cells.append(code("""raw = pd.read_excel(RAW_PATH, sheet_name='Sheet1-GSAF')
print(f'Raw shape: {raw.shape}')
raw.head()"""))
cells.append(code("""quality_before = pd.DataFrame({
    'dtype': raw.dtypes.astype(str),
    'missing': raw.isna().sum(),
    'unique': raw.nunique(dropna=True)
}).sort_values('missing', ascending=False)
quality_before"""))
cells.append(markdown("""## 2. Clean the data

The imported `clean_shark_data` function calls smaller reusable functions in a documented order. It standardizes columns and text, removes exact duplicates, parses dates and ages, standardizes categorical fields, and creates analytical groupings."""))
cells.append(code("""clean = clean_shark_data(raw)
print(f'Cleaned shape: {clean.shape}')
print(f'Exact rows removed: {len(raw) - len(clean)}')
clean.head()"""))
cells.append(code("""clean[['year', 'incident_date', 'age_numeric', 'age_group',
       'sex_clean', 'fatal', 'activity_group', 'incident_type']].head(10)"""))
cells.append(code("""clean.to_csv(ROOT / 'data' / 'cleaned' / 'shark_attacks_clean.csv', index=False)"""))
cells.append(markdown("""## 3. Define the analytical population

We select complete calendar years 2000–2025 and cases classified by GSAF as unprovoked. Excluding 2026 prevents a partial year from being compared with full years."""))
cells.append(code("""analysis = clean.loc[
    clean['year'].between(2000, 2025) &
    clean['incident_type'].eq('Unprovoked')
].copy()
print(f'Analysis rows: {len(analysis):,}')"""))
cells.append(markdown("## 4. Exploratory data analysis"))
cells.append(code("""activity_counts = analysis['activity_group'].value_counts()
activity_counts"""))
cells.append(code("""ax = activity_counts.sort_values().plot.barh(figsize=(10, 6), color='#136F63')
ax.set_title('Recorded unprovoked shark incidents by activity, 2000–2025', weight='bold')
ax.set_xlabel('Number of recorded incidents'); ax.set_ylabel('')
plt.tight_layout(); plt.show()"""))
cells.append(code("""country_counts = analysis['country'].fillna('Unknown').value_counts().head(10)
country_counts"""))
cells.append(code("""ax = country_counts.sort_values().plot.barh(figsize=(10, 6), color='#D97706')
ax.set_title('Top countries by recorded unprovoked incidents, 2000–2025', weight='bold')
ax.set_xlabel('Number of recorded incidents'); ax.set_ylabel('')
plt.tight_layout(); plt.show()"""))
cells.append(code("""known_fatal = analysis[analysis['fatal'].isin(['Yes', 'No'])]
fatal_by_activity = (known_fatal.groupby('activity_group')['fatal']
                     .apply(lambda x: x.eq('Yes').mean() * 100)
                     .sort_values(ascending=False))
print(f'Known outcomes: {len(known_fatal):,}')
print(f'Overall fatal percentage: {known_fatal["fatal"].eq("Yes").mean() * 100:.2f}%')
fatal_by_activity"""))
cells.append(code("""annual = analysis.groupby('year').size()
ax = annual.plot(figsize=(10, 5), marker='o', color='#136F63')
ax.set_title('Recorded unprovoked incidents over time', weight='bold')
ax.set_ylabel('Recorded incidents'); ax.set_xlabel('Year')
plt.tight_layout(); plt.show()"""))
cells.append(markdown("""## 5. Conclusion

The hypothesis is **supported within the selected data**: surfing is the most frequently recorded activity group, with **966 of 2,220** modern unprovoked incidents. The USA has the highest recorded count (**1,125**). Among 2,203 records with known outcomes, **10.80%** are fatal.

These figures do not measure personal risk or establish causation. Reporting levels, coastline usage, population, tourism, and participation rates vary substantially. Actual risk estimation would require exposure denominators such as participant-hours by activity and location."""))

nb["cells"] = cells
out = root / "notebooks" / "shark_attacks_analysis.ipynb"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(out)
