# Release kit

Outputs built from the aggregate tables in `results/`, so every number matches the preprint
([doi:10.20944/preprints202611.0240.v1](https://doi.org/10.20944/preprints202611.0240.v1)).

| File | What it is |
| --- | --- |
| `findings.csv` | Eight headline findings (F1–F8), with the number as printed by the script, its scope and its source table |
| `build_explorer_data.py` | Reads `results/` and writes `explorer/data.json`, `explorer/tables/*.csv` and `findings.csv`; checks the totals (854,785 articles, 378,955 open) |
| `build_explorer_page.py` | Puts the data and the map into `explorer/template.html` and writes `explorer/index.html` (standalone) and `explorer/site/oa-africa.qmd` (CognosX website) |
| `explorer/tables/` | The eight aggregate tables behind the explorer (CC BY 4.0) |
| `explorer/africa.geo.json` | Country shapes from Natural Earth via world-atlas 2.0.2 (public domain) |

Rebuild:

```bash
python release/build_explorer_data.py
python release/build_explorer_page.py
```

Yearly data by region, country and collaboration type are not in the explorer: those tables come from an
earlier extract that lacks 16,084 articles from 2019–2021 (see `docs/methods.md`).
