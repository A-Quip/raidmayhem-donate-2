# raidmayhem-donate-2

A standalone public donate page for a RaidMayhem stream. Prices, tip URL, and effects
all come from `config.yml` — the page is regenerated from it, so what's advertised can't
drift from the values you set.

- `config.yml` — tip URL, effects, caps, and the mob/item price lists.
- `build_page.py` — reads `config.yml` and writes `index.html`. Edit `config.yml`, then
  run `python build_page.py`.
- `index.html` — the generated page (committed so it renders on GitHub without CI).
- Deployed to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

## Setup

1. Set `site.tip-url` in `config.yml` to the StreamElements tip page, adjust prices,
   run `python build_page.py`, commit, push.
2. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**
   (only if the workflow's auto-enable didn't already turn it on).
3. The page publishes to `https://<user>.github.io/raidmayhem-donate-2/`. Put that URL
   in the chatbot's `!donate` command.

Changing a price later = edit `config.yml`, push — the page redeploys itself.
