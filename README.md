# tsa-nps-spending-2024-data

Frozen 2024 visitor-spending breakdowns and headline metrics for the TSA NPS notebook, replacing the notebook’s live VSE API calls with versioned CSV snapshots.

## Upstream Sources
- NPS Visitor Spending Effects nation-result API for 2024
- NPS Visitor Spending Effects park-result API for Great Smoky Mountains (GRSM)

## Processing Summary
The preprocessed layer freezes raw sector-level visitor-spending values plus the 2024 totals returned by the VSE API. The postprocessed layer creates the eight-slice pie-chart table and the four headline metrics consumed by the notebook.

## Available Versions
- `v1` is included in this repo.
- Future refreshes should be added as `Data/v2/...`, `Data/v3/...`, and so on without removing older versions.

## Current Version File Inventory
### Preprocessed
| File | Rows | Columns |
| --- | --- | --- |
| national_vse_sectors_visitor_spending_2024.csv | 8 | 2 |
| national_vse_totals_2024.csv | 8 | 3 |
| great_smoky_vse_totals_2024.csv | 8 | 3 |

### Postprocessed
| File | Rows | Columns |
| --- | --- | --- |
| spending_sector_breakdown_2024.csv | 8 | 6 |
| spending_highlights_2024.csv | 4 | 4 |

## Current Version Row Counts
### Preprocessed
| File | Rows | Columns |
| --- | --- | --- |
| national_vse_sectors_visitor_spending_2024.csv | 8 | 2 |
| national_vse_totals_2024.csv | 8 | 3 |
| great_smoky_vse_totals_2024.csv | 8 | 3 |

### Postprocessed
| File | Rows | Columns |
| --- | --- | --- |
| spending_sector_breakdown_2024.csv | 8 | 6 |
| spending_highlights_2024.csv | 4 | 4 |

## Preprocessed Data Dictionary

### `national_vse_sectors_visitor_spending_2024.csv`

| column | type | description | example_or_unit |
| --- | --- | --- | --- |
| sector_name | string | Visitor-spending sector name returned by the VSE API. | Lodging |
| visitor_spending_dollars | float | 2024 spending value for the sector in nominal dollars. | 8994513365.0 dollars |

### `national_vse_totals_2024.csv`

| column | type | description | example_or_unit |
| --- | --- | --- | --- |
| category | string | Top-level VSE metric category. | Economic Output |
| total_year | integer | Year of the total returned by the API. | 2024 |
| total_value | float | Category total for that year. | 56327363830.0 |

### `great_smoky_vse_totals_2024.csv`

| column | type | description | example_or_unit |
| --- | --- | --- | --- |
| category | string | Top-level VSE metric category for Great Smoky Mountains. | Visitor Spending |
| total_year | integer | Year of the total returned by the API. | 2024 |
| total_value | float | Park-level total for that year. | 2367391541.0 |

## Postprocessed Data Dictionary

### `spending_sector_breakdown_2024.csv`

| column | type | description | example_or_unit |
| --- | --- | --- | --- |
| sector_name | string | Original sector name from the VSE API. | Recreation Industries |
| chart_label | string | Notebook display label for the pie chart. | Recreation |
| visitor_spending_dollars | float | 2024 visitor spending for the sector in dollars. | 2478817852.0 dollars |
| visitor_spending_billions | float | 2024 visitor spending for the sector in billions of dollars. | 2.48 billion dollars |
| share_pct | float | Sector share of total visitor spending across the eight displayed sectors. | 8.54 percent |
| plot_order | integer | Fixed pie-chart order used by the notebook. | 6 |

### `spending_highlights_2024.csv`

| column | type | description | example_or_unit |
| --- | --- | --- | --- |
| metric_key | string | Stable machine-readable metric identifier. | national_jobs_supported |
| metric_label | string | Human-readable metric label shown in notebook outputs. | Jobs supported |
| value | float | Metric value stored as a numeric field. | 415400.0 |
| unit | string | Unit for the metric value. | jobs |
