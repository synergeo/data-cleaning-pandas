"""Run the SharkSafe cleaning, analysis, exports, and chart generation."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from cleaning import load_and_clean


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "GSAF5.xls"
CLEAN_PATH = ROOT / "data" / "cleaned" / "shark_attacks_clean.csv"
OUTPUT = ROOT / "outputs"


def save_bar(series: pd.Series, title: str, xlabel: str, filename: str, color: str = "#136F63") -> None:
    fig, ax = plt.subplots(figsize=(10, 6))
    series.sort_values().plot.barh(ax=ax, color=color)
    ax.set_title(title, fontsize=15, weight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(ax.containers[0], padding=3, fmt="%.0f")
    fig.tight_layout()
    fig.savefig(OUTPUT / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run() -> None:
    (ROOT / "data" / "cleaned").mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    df = load_and_clean(RAW_PATH)
    df.to_csv(CLEAN_PATH, index=False)

    # Complete years only, recent enough to reflect modern reporting; unprovoked cases only.
    analysis = df.loc[
        df["year"].between(2000, 2025)
        & df["incident_type"].eq("Unprovoked")
    ].copy()

    activities = analysis["activity_group"].value_counts()
    countries = analysis["country"].fillna("Unknown").value_counts().head(10)
    known_fatal = analysis.loc[analysis["fatal"].isin(["Yes", "No"])]
    fatal_by_activity = (
        known_fatal.groupby("activity_group", observed=True)["fatal"]
        .apply(lambda x: x.eq("Yes").mean() * 100)
        .sort_values(ascending=False)
    )

    summary = pd.DataFrame(
        {
            "metric": [
                "Raw rows", "Cleaned rows", "Analysis rows", "Analysis period",
                "Most recorded activity", "Most recorded country",
                "Known fatal outcomes", "Overall fatal percentage (known outcomes)",
            ],
            "value": [
                len(pd.read_excel(RAW_PATH, sheet_name="Sheet1-GSAF")),
                len(df), len(analysis), "2000–2025",
                f"{activities.index[0]} ({activities.iloc[0]:,})",
                f"{countries.index[0]} ({countries.iloc[0]:,})",
                f"{len(known_fatal):,}",
                f"{known_fatal['fatal'].eq('Yes').mean() * 100:.2f}%",
            ],
        }
    )
    summary.to_csv(OUTPUT / "summary_metrics.csv", index=False)
    activities.rename_axis("activity_group").reset_index(name="incidents").to_csv(
        OUTPUT / "incidents_by_activity.csv", index=False
    )
    countries.rename_axis("country").reset_index(name="incidents").to_csv(
        OUTPUT / "top_countries.csv", index=False
    )
    fatal_by_activity.rename("fatal_percent").reset_index().to_csv(
        OUTPUT / "fatal_percentage_by_activity.csv", index=False
    )

    save_bar(
        activities, "Recorded unprovoked shark incidents by activity, 2000–2025",
        "Number of recorded incidents", "01_activity_counts.png",
    )
    save_bar(
        countries, "Top countries by recorded unprovoked incidents, 2000–2025",
        "Number of recorded incidents", "02_top_countries.png", "#D97706",
    )
    save_bar(
        fatal_by_activity, "Fatal outcomes by activity (known outcomes), 2000–2025",
        "Fatal outcomes (%)", "03_fatal_by_activity.png", "#B91C1C",
    )

    annual = analysis.groupby("year", observed=True).size()
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(annual.index, annual.values, marker="o", linewidth=2, color="#136F63")
    ax.set_title("Recorded unprovoked incidents over time", fontsize=15, weight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Recorded incidents")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT / "04_incidents_over_time.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    run()

