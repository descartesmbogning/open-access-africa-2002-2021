# Data

No article-level data are stored in this repository.

## Why

The sample comes from the Web of Science Core Collection, whose licence does not allow raw records to be redistributed. The intermediate files built from it (pickle and CSV files of 0.4 to 6 GB) also contain those records, so they stay private.

## How to rebuild the sample

1. Search the Web of Science Core Collection for records whose addresses contain an African country or major African city (export date in 2022, years 1975–2021), and export full records.
2. Run `notebooks/01_sample_and_countries/analyse_based_on_wos_affil_only_part1_group.ipynb` to keep records with an African address and to extract countries and regions.
3. Run `notebooks/01_sample_and_countries/analyse_based_on_wos_affil_only_part3_finance.ipynb` for the funding flag.
4. Query Unpaywall for every DOI with `notebooks/02_unpaywall_harvest/open_access_scopus.ipynb`.
5. Run the notebooks in `04_merge_and_variables`, then `05_analysis`.

Note that Unpaywall changed its classification code in May 2025, so a new query will not reproduce the August 2022 OA statuses exactly.

## What can be shared later

A DOI-level file with the Unpaywall OA status (August 2022) and derived variables (year, countries, region, collaboration type, funding flag) does not contain Web of Science text and can be shared under CC BY 4.0. It is planned for a later release.
