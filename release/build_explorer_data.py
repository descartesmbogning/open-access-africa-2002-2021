"""Build the aggregate data behind the OA Africa explorer and the findings sheet.

Reads only the aggregate tables in results/ (final sample, 854,785 articles).
Writes:
  release/explorer/data.json      one bundle the explorer page reads
  release/explorer/tables/*.csv   the same data as tables people can download
  release/findings.csv            headline findings, numbers as printed by this script

Run from the repository root:  python release/build_explorer_data.py

Not used on purpose: region-by-year, country-by-year and collaboration-by-year
tables. They come from an earlier extract that lacks 16,084 articles from
2019-2021 (see docs/methods.md), so they would disagree with the preprint.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "results" / "tables"
F = ROOT / "results" / "figure_data"
OUT = ROOT / "release" / "explorer"
(OUT / "tables").mkdir(parents=True, exist_ok=True)

TYPES = ["gold", "green", "hybrid", "bronze"]

REGIONS = {
    "Northern Africa": ["Algeria", "Djibouti", "Egypt", "Libya", "Morocco", "Tunisia"],
    "Eastern Africa": ["Burundi", "Comoros", "Eritrea", "Ethiopia", "Kenya", "Madagascar",
                       "Mauritius", "Rwanda", "Seychelles", "Somalia", "South Sudan", "Sudan",
                       "Tanzania", "Uganda"],
    "Southern Africa": ["Angola", "Botswana", "Eswatini", "Lesotho", "Malawi", "Mozambique",
                        "Namibia", "South Africa", "Zambia", "Zimbabwe"],
    "Western Africa": ["Benin", "Burkina Faso", "Cabo Verde", "Cote d'Ivoire", "Gambia", "Ghana",
                       "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Mauritania", "Niger",
                       "Nigeria", "Senegal", "Sierra Leone", "Togo"],
    "Central Africa": ["Cameroon", "Central African Republic", "Chad", "Congo Republic",
                       "DR Congo", "Equatorial Guinea", "Gabon", "Sao Tome and Principe"],
}
REGION_OF = {c: r for r, cs in REGIONS.items() for c in cs}
REGION_KEY = {"north_africa": "Northern Africa", "eastern_africa": "Eastern Africa",
              "Southern_africa": "Southern Africa", "Western_africa": "Western Africa",
              "Central_africa": "Central Africa"}
# ISO 3166-1 numeric codes, used to join the map geometry (world-atlas 2.0.2)
ISO = {"Algeria": "012", "Angola": "024", "Benin": "204", "Botswana": "072", "Burkina Faso": "854",
       "Burundi": "108", "Cabo Verde": "132", "Cameroon": "120", "Central African Republic": "140",
       "Chad": "148", "Comoros": "174", "Congo Republic": "178", "Cote d'Ivoire": "384",
       "DR Congo": "180", "Djibouti": "262", "Egypt": "818", "Equatorial Guinea": "226",
       "Eritrea": "232", "Eswatini": "748", "Ethiopia": "231", "Gabon": "266", "Gambia": "270",
       "Ghana": "288", "Guinea": "324", "Guinea-Bissau": "624", "Kenya": "404", "Lesotho": "426",
       "Liberia": "430", "Libya": "434", "Madagascar": "450", "Malawi": "454", "Mali": "466",
       "Mauritania": "478", "Mauritius": "480", "Morocco": "504", "Mozambique": "508",
       "Namibia": "516", "Niger": "562", "Nigeria": "566", "Rwanda": "646",
       "Sao Tome and Principe": "678", "Senegal": "686", "Seychelles": "690",
       "Sierra Leone": "694", "Somalia": "706", "South Africa": "710", "South Sudan": "728",
       "Sudan": "729", "Tanzania": "834", "Togo": "768", "Tunisia": "788", "Uganda": "800",
       "Zambia": "894", "Zimbabwe": "716"}


def r1(x):
    return round(float(x), 1)


# ---- Years (all document types, final sample) --------------------------------
isoa = pd.read_excel(T / "oa_general.xlsx", "is_oa_doc_types_year")
stat = pd.read_excel(T / "oa_general.xlsx", "oa_status_doc_types_year")
doc_cols = [c for c in isoa.columns if c not in ("Unnamed: 0", "is_oa")]
years = []
for y in range(2002, 2022):
    row = {"year": y}
    for lab in ("true", "false"):
        v = isoa[(isoa["Unnamed: 0"].astype(str) == str(y)) & (isoa["is_oa"] == lab)][doc_cols]
        row[lab] = int(v.sum(axis=1).iloc[0])
    for t in TYPES + ["closed"]:
        v = stat[(stat["publication_year"].astype(str) == str(y)) & (stat["oa_status"] == t)][doc_cols]
        row[t] = int(v.sum(axis=1).iloc[0])
    years.append({"year": y, "articles": row["true"] + row["false"], "oa": row["true"],
                  **{t: row[t] for t in TYPES}, "closed": row["closed"]})
yr = pd.DataFrame(years)
assert (yr[TYPES].sum(axis=1) == yr["oa"]).all(), "OA types do not add up to OA"
assert (yr["oa"] + yr["closed"] == yr["articles"]).all()
yr["oa_pct"] = (100 * yr.oa / yr.articles).round(1)
for t in TYPES:
    yr[f"{t}_pct_of_articles"] = (100 * yr[t] / yr.articles).round(1)
    yr[f"{t}_pct_of_oa"] = (100 * yr[t] / yr.oa).round(1)
TOTAL, OA = int(yr.articles.sum()), int(yr.oa.sum())
assert TOTAL == 854785 and OA == 378955, (TOTAL, OA)

# ---- Regions (full counting) ---------------------------------------------------
rg = pd.read_excel(T / "oa_general.xlsx", "oa_status_region").rename(columns={"Unnamed: 0": "key"})
rg["region"] = rg.key.map(REGION_KEY)
rg["articles"] = rg[TYPES + ["closed"]].sum(axis=1)
rg["oa"] = rg[TYPES].sum(axis=1)
rg["oa_pct"] = (100 * rg.oa / rg.articles).round(1)
for t in TYPES:
    rg[f"{t}_pct"] = (100 * rg[t] / rg.articles).round(1)
regions = rg[["region", "articles", "oa", "oa_pct"] + [f"{t}_pct" for t in TYPES]]

# ---- Countries (full counting, 54) ---------------------------------------------
ct = pd.read_excel(T / "oa_general.xlsx", "countries").rename(columns={"Unnamed: 0": "country"})
ct["articles"] = ct["true"] + ct["false"]
ct["oa"] = ct["true"]
ct["oa_pct"] = (100 * ct.oa / ct.articles).round(1)
ct["z"] = ct["true_%_z_score"].round(2)
for t in TYPES:
    ct[f"{t}_pct"] = (100 * ct[t] / ct.articles).round(1)
ct["region"] = ct.country.map(REGION_OF)
ct["iso"] = ct.country.map(ISO)
assert ct.region.notna().all() and ct.iso.notna().all() and len(ct) == 54
countries = ct[["country", "iso", "region", "articles", "oa", "oa_pct", "z"] +
               [f"{t}_pct" for t in TYPES]].sort_values("oa_pct", ascending=False)

# ---- Research areas (152 WoS areas, an article counts in each of its areas) ----
fa = pd.read_excel(T / "oa_general_research_area.xlsx", "Feuil2").rename(columns={"Unnamed: 0": "area"})
fa["articles"] = fa["total"]
fa["oa_pct"] = fa["true_%"].round(1)
for t in TYPES:
    fa[f"{t}_pct"] = fa[f"{t}_%"].round(1)
fields = fa[["area", "articles", "oa_pct"] + [f"{t}_pct" for t in TYPES]].sort_values("oa_pct", ascending=False)

# ---- Collaboration types ---------------------------------------------------------
co = pd.read_excel(T / "oa_collaboration.xlsx", "Feuil8").rename(columns={"Unnamed: 0": "key"})
CO_LABEL = {"international_collaborations": "International", "continental_collaborations": "Continental",
            "regional_collaborations": "Regional", "national_collaborations": "National"}
co["type"] = co.key.map(CO_LABEL)
co["articles"] = co[TYPES + ["closed"]].sum(axis=1)
co["oa"] = co[TYPES].sum(axis=1)
co["oa_pct"] = (100 * co.oa / co.articles).round(1)
for t in TYPES:
    co[f"{t}_pct"] = (100 * co[t] / co.articles).round(1)
collab = co[["type", "articles", "oa", "oa_pct"] + [f"{t}_pct" for t in TYPES]]
collab = collab.set_index("type").loc[["International", "Continental", "Regional", "National"]].reset_index()

# ---- Partner regions outside Africa (World Bank regions) -------------------------
cby = pd.read_csv(F / "collaboration_by_year.csv", header=None)
PARTNERS = {"wb_latin_america_and_the_caribbean": "Latin America & Caribbean",
            "wb_north_america": "North America", "wb_south_asia": "South Asia",
            "wb_east_asia_and_pacific": "East Asia & Pacific",
            "wb_europe_and_central_asia": "Europe & Central Asia",
            "wb_middle_east_and_north_africa_others": "Middle East (outside Africa)"}
prt = []
for k, lab in PARTNERS.items():
    r = cby[cby[0] == k].iloc[0]
    closed, oa = int(r[1]), int(r[2])
    prt.append({"partner_region": lab, "articles": closed + oa, "oa": oa,
                "oa_pct": round(100 * oa / (closed + oa), 1)})
partners = pd.DataFrame(prt).sort_values("oa_pct", ascending=False)

# ---- Funding --------------------------------------------------------------------
fu = pd.read_csv(F / "figure_8_funding.csv", header=None)
fund = []
for key, lab in (("fund", "Funded"), ("not_fund", "Not funded")):
    a = fu[fu[0] == key].iloc[0]   # first block: false, false_%, true, true_%, total
    b = fu[fu[0] == key].iloc[1]   # second block: gold, gold_%, green, ... closed, closed_%, count
    rec = {"funding": lab, "articles": int(a[5]), "oa": int(a[3]), "oa_pct": r1(a[4])}
    for i, t in enumerate(["gold", "green", "hybrid", "bronze"]):
        rec[f"{t}_pct"] = r1(b[2 + 2 * i])
    fund.append(rec)
funding = pd.DataFrame(fund)
assert funding.articles.sum() == TOTAL

# ---- Citations (WoS Times Cited, not normalised) --------------------------------
tc = pd.read_csv(F / "figure_9_times_cited.csv", header=None, dtype=str)
start = tc.index[(tc[1] == "year_group") & (tc[2] == "is_oa")][0]
cit = []
for i in range(start + 1, start + 9):
    r = tc.loc[i]
    cit.append({"period": r[1], "status": "Open access" if r[2] == "true" else "Closed",
                "mean_citations": r1(r[3]), "median_citations": int(float(r[6]))})
citations = pd.DataFrame(cit)

# ---- Export ---------------------------------------------------------------------
tables = {"oa_by_year": yr, "oa_by_region": regions, "oa_by_country": countries,
          "oa_by_research_area": fields, "oa_by_collaboration_type": collab,
          "oa_by_partner_region": partners, "oa_by_funding": funding,
          "citations_by_period": citations}
for name, df in tables.items():
    df.to_csv(OUT / "tables" / f"{name}.csv", index=False)

meta = {"articles": TOTAL, "oa": OA, "oa_pct": r1(100 * OA / TOTAL),
        "period": "2002-2021", "oa_measured": "August 2022",
        "country_mean": r1(countries.oa_pct.mean()), "country_sd": r1(ct.oa_pct.std()),
        "country_median": r1(countries.oa_pct.median()), "n_countries": len(countries)}
bundle = {"meta": meta, **{k: v.to_dict(orient="records") for k, v in tables.items()}}
(OUT / "data.json").write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")))

# ---- Findings sheet -------------------------------------------------------------
y = yr.set_index("year")
reg = regions.set_index("region")
col = collab.set_index("type")
fun = funding.set_index("funding")
top, low = countries.iloc[0], countries.iloc[-1]
c1 = citations.set_index(["period", "status"])
findings = [
    ("F1", "Almost half of African-affiliated articles were free to read in August 2022.",
     f"{meta['oa_pct']}% ({OA:,} of {TOTAL:,})", "WoS articles with an African address and a DOI, 2002-2021; OA status from Unpaywall, Aug 2022",
     "oa_by_year (sum)", "Headline number", "All"),
    ("F2", "The yearly share of open articles more than tripled in twenty years.",
     f"{y.loc[2002, 'oa_pct']}% (2002) to {y.loc[2020, 'oa_pct']}% (2020) and {y.loc[2021, 'oa_pct']}% (2021)",
     f"n = {y.loc[2002, 'articles']:,} articles in 2002 and {y.loc[2021, 'articles']:,} in 2021", "oa_by_year; Fig 1", "Line", "All"),
    ("F3", "Most open articles are published in fully open journals (Gold).",
     f"{y.loc[2021, 'gold_pct_of_oa']}% of OA articles in 2021", f"n = {y.loc[2021, 'oa']:,} OA articles in 2021", "oa_by_year; Fig 2", "Stacked area", "Researchers, funders"),
    ("F4", "Open access differs widely between African regions.",
     f"{reg.loc['Eastern Africa', 'oa_pct']}% (Eastern) vs {reg.loc['Northern Africa', 'oa_pct']}% (Northern)",
     "Full counting; 2002-2021", "oa_by_region; Fig 3A", "Bar", "Policy makers"),
    ("F5", "Country shares range from under a third to over three quarters.",
     f"{low.oa_pct}% ({low.country}) to {top.oa_pct}% ({top.country})",
     f"54 countries; mean {meta['country_mean']}%, SD {meta['country_sd']}; small countries (<500 articles) vary more", "oa_by_country; Fig 4A", "Map + ranking", "Policy makers"),
    ("F6", "Articles with a co-author outside Africa are more often open.",
     f"{col.loc['International', 'oa_pct']}% vs {col.loc['National', 'oa_pct']}% (single country)",
     f"n = {col.loc['International', 'articles']:,} international, {col.loc['National', 'articles']:,} national; descriptive", "oa_by_collaboration_type; Fig 6A", "Bar", "Researchers, funders"),
    ("F7", "Funded articles are more often open than unfunded ones.",
     f"{fun.loc['Funded', 'oa_pct']}% vs {fun.loc['Not funded', 'oa_pct']}%",
     "Funding = WoS Funding Orgs field not empty; under-recorded before 2008; descriptive", "oa_by_funding; Fig 8A", "Bar", "Funders"),
    ("F8", "Open articles have higher mean citations, without adjustment for field or journal.",
     f"{c1.loc[('2002-2006', 'Open access'), 'mean_citations']} vs {c1.loc[('2002-2006', 'Closed'), 'mean_citations']} (2002-2006)",
     "WoS Times Cited at export (2022); not normalised; association only", "citations_by_period; Fig 9A", "Dot plot", "Researchers"),
]
fs = pd.DataFrame(findings, columns=["ID", "Finding", "Number", "Uncertainty and scope", "Source", "Chart", "Audience"])
fs["Used in"] = "explorer"
fs.to_csv(ROOT / "release" / "findings.csv", index=False)
print(fs[["ID", "Number"]].to_string(index=False))
print(json.dumps(meta))
