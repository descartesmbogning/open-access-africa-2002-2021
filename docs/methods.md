# Methods notes

These notes record how the variables were built, as read from the notebooks. Counts come from the saved notebook outputs.

## Record flow

| Step | Records | Removed |
| --- | --- | --- |
| Web of Science Core Collection records matching African country and city names, 1975–2021 | 1,416,524 | |
| At least one African institutional address, after affiliation checks | 1,269,130 | 147,394 |
| With a DOI | 978,142 | 290,988 without DOI |
| Published 2002–2021 | 881,625 | 96,517 outside the window |
| With an Unpaywall OA status (August 2022) | **854,785** | 26,840 not found in Unpaywall |

Source: `notebooks/04_merge_and_variables/open_access_analyses_2.ipynb`.

### DOI enrichment (not used)

`notebooks/03_doi_enrichment_not_used` matched records without a DOI to Scopus, Lens and Crossref. This recovered 30,633 DOIs (290,988 records without DOI before, 260,355 after). The recovered DOIs were not sent to Unpaywall, so the enriched records have no OA status and are not part of the 854,785 articles. The step is kept here for transparency.

## Open access status

OA status comes from the Unpaywall API v2 (`oa_status` and `is_oa`), queried by DOI in August 2022. Each article has one status, following Unpaywall's order of priority: gold, hybrid, bronze, green, closed.

## Countries and regions

Countries come from the institutional addresses of all authors (`notebooks/01_sample_and_countries/analyse_based_on_wos_affil_only_part1_group.ipynb`). Counting is full: an article with authors in several countries counts once for each country.

African regions (54 countries):

| Region | Countries |
| --- | --- |
| Northern Africa (6) | Algeria, Djibouti, Egypt, Libya, Morocco, Tunisia |
| Eastern Africa (14) | Burundi, Comoros, Eritrea, Ethiopia, Kenya, Madagascar, Mauritius, Rwanda, Seychelles, Somalia, South Sudan, Sudan, Tanzania, Uganda |
| Southern Africa (10) | Angola, Botswana, Eswatini, Lesotho, Malawi, Mozambique, Namibia, South Africa, Zambia, Zimbabwe |
| Western Africa (16) | Benin, Burkina Faso, Cabo Verde, Cote d'Ivoire, Gambia, Ghana, Guinea, Guinea-Bissau, Liberia, Mali, Mauritania, Niger, Nigeria, Senegal, Sierra Leone, Togo |
| Central Africa (8) | Cameroon, Central African Republic, Chad, Congo Republic, DR Congo, Equatorial Guinea, Gabon, Sao Tome and Principe |

Partner countries outside Africa are grouped by World Bank region and, separately, by SCImago world region.

## Collaboration types

Built in `notebooks/04_merge_and_variables/open_access_analyses_2_countries.ipynb`. Each article gets exactly one type, checked in this order:

1. **International**: at least one address outside Africa.
2. **Continental**: all addresses in Africa, in two or more African regions.
3. **Regional**: all addresses in one African region, in two or more countries.
4. **National**: all addresses in a single African country. Single-author articles fall here.

## Funding

Built in `notebooks/01_sample_and_countries/analyse_based_on_wos_affil_only_part3_finance.ipynb`. An article is `fund` when the Web of Science field *Funding Orgs* is not empty, and `not_fund` otherwise. In the final sample, 351,056 articles are funded (41.1%) and 503,729 are not. Web of Science records funding systematically only from 2008, so earlier years are under-recorded.

## Citations

Citation counts are the Web of Science *Times Cited, All Databases* values at export (2022). Means are reported by OA status within four periods (2002–2006, 2007–2011, 2012–2016, 2017–2021). They are not normalised by field or journal.

## z-scores

For each grouping (countries, regions, fields and so on), the share of OA articles in each group is standardised against the mean and standard deviation of that share across groups: z = (x − mean) / SD. With fewer than about five groups, the z-score carries little information and should not be read.
