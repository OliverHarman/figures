---
title: One national number covers very different places
slug: ggvc-argentina-natural-capital
date: 2026-10-06
status: published
description: Argentina's wealth per person in 2018 split by type and mobility, with eleven places where its natural capital is found.
used_in:
  - "World Economic Forum blog: Global supply chains run on local nature (submitted October 2026)"
related: Crescenzi and Harman (2026), Green Global Value Chains for Sustainable Development, https://doi.org/10.1017/9781009623766
---

## Sources
- National wealth: World Bank, Wealth Accounts (Changing Wealth of Nations, 2024 release), Argentina 2018, current US$ per person. Retrieved October 2026 from https://databank.worldbank.org/source/wealth-accounts
- Places: see `places.csv` (one source per row).
- Boundaries: Natural Earth admin-1 (public domain).
- Mobility labels: the authors' classification.

## Rebuild
`python build.py` regenerates `index.html` from `places.csv`, `wealth.csv`, `template.html` and `arg_prov.geojson`.
The bar labels and mobility brackets in `template.html` are positioned by hand; if `wealth.csv` changes, adjust them.

## Notes
- The book cites the 2021 edition (renewable natural capital about 10% of US$121,187). The 2024 release revises this to 6.5% of US$93,462.
- `static.png` is a screenshot of the interactive version for editors who need an image.
