"""Inject the aggregate data and the Africa map into the explorer template.
Run after build_explorer_data.py:  python release/build_explorer_page.py

Writes
  release/explorer/index.html          standalone page (light and dark)
  release/explorer/site/oa-africa.qmd  page for the CognosX website (Quarto, light),
                                       to copy into cognosx.ca/dashboards/ with the CSV
                                       tables in dashboards/files/oa-africa/
"""
import re
from pathlib import Path

D = Path(__file__).resolve().parent / "explorer"
tpl = (D / "template.html").read_text()
tpl = tpl.replace("/*__DATA__*/null", (D / "data.json").read_text())
tpl = tpl.replace("/*__GEO__*/null", (D / "africa.geo.json").read_text())

# Standalone: keep everything, drop the markers
standalone = re.sub(r"<!--/?STANDALONE-->|/\*/?STANDALONE\*/", "", tpl)
(D / "index.html").write_text(standalone)

# Website: drop standalone-only parts, point downloads to the site's CSV files
site = re.sub(r"<!--STANDALONE-->.*?<!--/STANDALONE-->", "", tpl, flags=re.S)
site = re.sub(r"/\*STANDALONE\*/.*?/\*/STANDALONE\*/", "", site, flags=re.S)
site = site.replace('<script src="https://cdnjs', '<script>window.OA_FILES="files/oa-africa/";</script>\n<script src="https://cdnjs', 1)
front = """---
title: "Open access in Africa, 2002–2021"
description: "Explore how much African research is free to read, by year, country, research area, collaboration and funding (854,785 articles)."
date: "2026-11-03"
categories: [Dashboard, Explorer, Open access]
projects: ["research-in-africa"]
page-layout: full
title-block-style: none
---

```{=html}
<style>#title-block-header{display:none} .cx-oa{margin-top:12px} .cx-oa .hero{border-radius:14px}</style>
"""
(D / "site").mkdir(exist_ok=True)
(D / "site" / "oa-africa.qmd").write_text(front + site + "\n```\n")
print("index.html", len(standalone) // 1024, "KB; oa-africa.qmd", len(site) // 1024, "KB")
