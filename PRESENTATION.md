# SharkSafe — 5-minute presentation

## Slide 1 — Title (10 seconds)

**SharkSafe**  
Cleaning and exploring global shark incidents  
Paul Omogiate Obamwonyi and project team

Speaker note: “We transformed a messy historical incident log into a reproducible analysis of where and during which activities modern unprovoked shark incidents are most frequently recorded.”

## Slide 2 — Question and hypothesis (20 seconds)

**Question:** Which activities and locations appear most frequently in modern unprovoked shark incidents?

**Hypothesis:** Surfing will be the most frequently recorded activity.

Speaker note: “We analyse recorded incidents, not actual risk, because we do not know how many people participated in each activity.”

## Slide 3 — The raw-data challenge (25 seconds)

- 7,117 raw records
- 23 original columns
- Historical and incomplete records
- Missing values and inconsistent categories
- Free-text ages, dates, activities, and fatal indicators

Visual: small before-cleaning table screenshot.

## Slide 4 — Reusable cleaning pipeline (30 seconds)

- Standardized column names
- Removed empty fields and duplicates
- Normalized strings and categories
- Parsed years and dates
- Extracted ages with regex
- Grouped activities with documented regex rules
- Created month, decade, age group, and fatal fields

Speaker note: “Instead of editing values manually, we wrote reusable functions and combined them into one ordered cleaning pipeline.”

## Slide 5 — Activity result (35 seconds)

Visual: `outputs/01_activity_counts.png`

Headline: **Surfing leads the selected records: 966 incidents**

Speaker note: “In the 2,220 unprovoked incidents from 2000 to 2025, surfing was the largest activity group. This supports our hypothesis within the selected dataset.”

## Slide 6 — Location result (25 seconds)

Visual: `outputs/02_top_countries.png`

Headline: **The USA has the most recorded incidents: 1,125**

Speaker note: “This may reflect both exposure and reporting differences. It must not be presented as a direct country-level risk ranking.”

## Slide 7 — Outcomes and context (25 seconds)

Visual: `outputs/03_fatal_by_activity.png`

- 2,203 records have a known fatal status
- 10.80% are fatal among known outcomes
- Outcome patterns differ by activity group

Speaker note: “We excluded unknown outcomes from the percentage denominator instead of treating them as nonfatal.”

## Slide 8 — Biggest obstacle (20 seconds)

**Free text is not analysis-ready.**

Examples: multiple spellings, detailed activity descriptions, nonnumeric ages, and inconsistent date formats.

Lesson: category rules should be transparent, reproducible, and easy to revise.

## Slide 9 — Conclusion and limitations (20 seconds)

- Hypothesis supported for recorded modern unprovoked incidents
- Surfing is the largest activity category
- USA is the leading recorded country
- Counts are not probabilities or proof of causation
- Exposure data would be needed to estimate actual risk

## Slide 10 — Thank you (10 seconds)

**SharkSafe**  
From messy records to careful evidence

## Two-minute demonstration

1. Show `df.head()` and `df.info()` for the raw dataset.
2. Open `src/cleaning.py` and point to `clean_shark_data()`.
3. Run the notebook’s pipeline cell.
4. Show raw versus cleaned dimensions.
5. Display the activity and country charts.
6. End with the limitation: incidents are not equivalent to risk.

