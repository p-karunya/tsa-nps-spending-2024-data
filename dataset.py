from pathlib import Path

import pandas as pd


PREPROCESSED_FILES = ['national_vse_sectors_visitor_spending_2024.csv', 'national_vse_totals_2024.csv', 'great_smoky_vse_totals_2024.csv']
POSTPROCESSED_FILES = ['spending_sector_breakdown_2024.csv', 'spending_highlights_2024.csv']
EXPECTED_PRE_ROWS = {'national_vse_sectors_visitor_spending_2024.csv': 8, 'national_vse_totals_2024.csv': 8, 'great_smoky_vse_totals_2024.csv': 8}
EXPECTED_POST_ROWS = {'spending_sector_breakdown_2024.csv': 8, 'spending_highlights_2024.csv': 4}


def _stage_dir(stage, version="v1", base_path="Data"):
    return Path(base_path) / version / stage


def _load_files(stage, filenames, version="v1", base_path="Data"):
    stage_path = _stage_dir(stage, version=version, base_path=base_path)
    return {name: pd.read_csv(stage_path / name) for name in filenames}


def load_preprocessed(version="v1", base_path="Data"):
    return _load_files("preprocessed", PREPROCESSED_FILES, version=version, base_path=base_path)


def load_postprocessed(version="v1", base_path="Data"):
    return _load_files("postprocessed", POSTPROCESSED_FILES, version=version, base_path=base_path)


def build_postprocessed(version="v1", base_path="Data"):
    pre = load_preprocessed(version=version, base_path=base_path)
    sectors = pre["national_vse_sectors_visitor_spending_2024.csv"].copy()
    totals = pre["national_vse_totals_2024.csv"].copy()
    great_smoky = pre["great_smoky_vse_totals_2024.csv"].copy()

    label_map = {
        "Lodging": "Lodging",
        "Restaurants": "Restaurants",
        "Gas": "Gas",
        "Groceries": "Groceries",
        "Retail": "Retail",
        "Recreation Industries": "Recreation",
        "Transportation": "Transportation",
        "Camping": "Camping",
    }
    order_map = {name: idx for idx, name in enumerate(label_map, start=1)}

    sectors["chart_label"] = sectors["sector_name"].map(label_map)
    sectors["plot_order"] = sectors["sector_name"].map(order_map)
    sectors = sectors.sort_values("plot_order").reset_index(drop=True)
    total_spending = sectors["visitor_spending_dollars"].sum()
    sectors["visitor_spending_billions"] = sectors["visitor_spending_dollars"] / 1e9
    sectors["share_pct"] = sectors["visitor_spending_dollars"] / total_spending * 100
    sectors = sectors[
        [
            "sector_name",
            "chart_label",
            "visitor_spending_dollars",
            "visitor_spending_billions",
            "share_pct",
            "plot_order",
        ]
    ]

    nation_lookup = totals.set_index("category")["total_value"]
    great_smoky_lookup = great_smoky.set_index("category")["total_value"]
    highlights = pd.DataFrame(
        [
            {
                "metric_key": "national_visitor_spending_billion",
                "metric_label": "Total NPS visitor spending",
                "value": nation_lookup["Visitor Spending"] / 1e9,
                "unit": "billion_usd_2024",
            },
            {
                "metric_key": "national_jobs_supported",
                "metric_label": "Jobs supported",
                "value": nation_lookup["Jobs"],
                "unit": "jobs",
            },
            {
                "metric_key": "national_economic_output_billion",
                "metric_label": "Total economic output",
                "value": nation_lookup["Economic Output"] / 1e9,
                "unit": "billion_usd_2024",
            },
            {
                "metric_key": "great_smoky_economic_output_billion",
                "metric_label": "Great Smoky economic output",
                "value": great_smoky_lookup["Economic Output"] / 1e9,
                "unit": "billion_usd_2024",
            },
        ]
    )
    return {
        "spending_sector_breakdown_2024.csv": sectors,
        "spending_highlights_2024.csv": highlights,
    }


def validate_schema(version="v1", base_path="Data"):
    loaded_pre = load_preprocessed(version=version, base_path=base_path)
    loaded_post = load_postprocessed(version=version, base_path=base_path)
    built_post = build_postprocessed(version=version, base_path=base_path)

    for name, df in loaded_pre.items():
        if len(df) != EXPECTED_PRE_ROWS[name]:
            raise ValueError(f"Unexpected row count for preprocessed file {name}: {len(df)} != {EXPECTED_PRE_ROWS[name]}")

    for name, df in loaded_post.items():
        if len(df) != EXPECTED_POST_ROWS[name]:
            raise ValueError(f"Unexpected row count for postprocessed file {name}: {len(df)} != {EXPECTED_POST_ROWS[name]}")
        if list(df.columns) != list(built_post[name].columns):
            raise ValueError(f"Column mismatch for postprocessed file {name}")

    return True


if __name__ == "__main__":
    validate_schema()
    print("Schema validation passed.")
