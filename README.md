# Interactive figures

Self-contained interactive figures (one HTML file each), published with GitHub Pages and listed on a catalogue page.

## Layout
```
figures/<slug>/
  index.html     the interactive figure (self-contained: no external scripts)
  static.png     an image version for editors
  README.md      front matter (title, date, status, used_in) + sources and notes
  *.csv          the data behind the figure
  build.py       regenerates index.html from the data (optional but encouraged)
templates/README.md   copy this when starting a new figure
build_index.py        builds _site/ (catalogue + published figures)
```

## Publish
1. Set `status: published` in the figure's README.
2. Commit and push to `main`. The workflow in `.github/workflows/pages.yml` builds `_site/` and deploys it.
3. The figure appears at `https://<user>.github.io/<repo>/<slug>/` and on the catalogue page.

Drafts (`status: draft`) stay in the repository but are not deployed. Preview everything locally with
`python build_index.py --all` and open `_site/index.html`.

## One-time setup
- Settings → Pages → Build and deployment → Source: **GitHub Actions**.
- Optional custom domain (e.g. `figures.oliverharman.me`): add it under Settings → Pages and create a CNAME record with your DNS provider pointing to `<user>.github.io`.

The repository is public. Keep unfinished work as `draft` or in a private repository.
