# Open Access in Africa, 2002–2021

Code, figure data and figures for the preprint:

> Mbogning Fonkou, M. D. *The Open Access Landscape in Africa: A Two-Decade Data Driven Analysis of Access, Impact, and Collaboration.* AfricArXiv (2026). DOI: to be added.

The study measures how much African research is openly available. It matches 854,785 articles with at least one African institutional address, indexed in the Web of Science Core Collection and published 2002–2021, to their open access (OA) status in Unpaywall (queried August 2022). It describes OA by year, OA type, country, region, discipline, collaboration type, funding and citations.

## Main results

- The share of articles available as OA rose from 16.7% (2002) to 58.7% (2021).
- Gold OA made up 70.2% of OA articles in 2021.
- OA ranged from 61.5% in Eastern Africa to 33.9% in Northern Africa.
- 63% of articles with a non-African co-author were OA in 2021, against 52.5% for single-country articles.
- 56.9% of funded articles were OA, against 35.6% of unfunded ones.

## Pipeline

| Step | Folder | What it does |
| --- | --- | --- |
| 1 | `notebooks/01_sample_and_countries` | Reads the Web of Science export, keeps articles with an African address, extracts countries from author addresses, assigns African regions and partner regions, builds the funding flag |
| 2 | `notebooks/02_unpaywall_harvest` | Merges DOIs and queries the Unpaywall API (v2) for each DOI, in batches of 1,000 |
| 3 | `notebooks/03_doi_enrichment_not_used` | Tried to recover missing DOIs from Scopus, Lens and Crossref. **Not used in the final analysis** (see `docs/methods.md`) |
| 4 | `notebooks/04_merge_and_variables` | Joins OA status to the sample, applies the DOI and 2002–2021 filters, builds collaboration types and period groups |
| 5 | `notebooks/05_analysis` | Counts, shares and z-scores by year, country, region, field, collaboration, funding, language, income group, colonial history, partner region and repository |

`docs/methods.md` gives the record flow, the definitions and the country lists. `docs/notebook_index.md` lists every notebook with what it reads and writes.

## Results

- `results/figures/`: the figures of the preprint (Figures 1 to 9).
- `results/figure_data/`: the numbers behind each figure, one CSV per figure, plus the original workbook `figure_source_data.xlsx`.
- `results/tables/`: aggregate tables by country, region, field, journal, publisher, language, income group, collaboration and funding.

All files in `results/` are aggregates. None holds article-level records.

## Running the notebooks

The notebooks were run locally in 2022–2023 with Python 3.8 and Jupyter. They read and write files with the absolute Windows paths used at the time (for example `D:\RESEARCH IN AFRICA\...`). To re-run them, change those paths to your own folders. The environment is in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate oa-africa
```

The Unpaywall API asks for an email address in each request. Replace `your_email@example.com` with your own.

## Data

Raw Web of Science records cannot be shared under the Clarivate licence, so they are not in this repository. `data/README.md` explains how to rebuild the sample. Unpaywall data are available under CC0.

## Licence

Code: MIT (`LICENSE`). Figures, figure data and tables: CC BY 4.0 (`LICENSE-data.md`).

## Citation

See `CITATION.cff`, or cite the preprint above.

## Contact

Maxime Descartes Mbogning Fonkou, CognosX, Burnaby, Canada. ORCID [0000-0001-5581-3891](https://orcid.org/0000-0001-5581-3891). Email: cognosxx@gmail.com
