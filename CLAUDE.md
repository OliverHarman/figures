# Figures repository: instructions for Claude Code

This repository holds Oliver Harman's interactive figures, deployed to GitHub Pages.

## Rules
- One folder per figure under `figures/<slug>/`. Slugs are lowercase-with-hyphens, prefixed by project (e.g. `ggvc-`, `cam-`).
- Every figure folder must contain `index.html`, `README.md` (front matter as in `templates/README.md`) and the data it uses. Add `static.png` for editors.
- `index.html` must be fully self-contained: inline CSS and JS, inline SVG, no external scripts, fonts or images, no browser storage. It must work when opened from disk.
- Follow the dataviz conventions already used in `figures/ggvc-argentina-natural-capital/template.html`: light and dark tokens, a legend for two or more series, hover AND tap AND keyboard focus for details, a "show as table" fallback, sources at the bottom.
- Every number shown must trace to a source listed in the figure's README or data file. Do not invent or round beyond the source.
- Prose (titles, descriptions, tooltips) follows Oliver's prose-register rules: plain language, British spelling, no "not A but B", no triads written for rhythm, sparing use of colons.
- New figures start as `status: draft`. Only change to `published` when Oliver says so.
- Never force-push; never delete a published figure without asking. When a figure is used somewhere new, add a line to `used_in`.

## Common tasks
- Rebuild a figure: `python figures/<slug>/build.py`
- Preview the site, drafts included: `python build_index.py --all`, then open `_site/index.html`
- Take a static screenshot (requires Playwright): open the figure, select a representative state, save as `static.png`.
