# raidmayhem-donate-2

A standalone public donate page for a RaidMayhem stream. Prices, tip URL, and effects
all come from `config.yml` — the page is regenerated from it, so what's advertised can't
drift from the values you set.

- `config.yml` — tip URL, effects, caps, and the mob/item price lists.
- `build_page.py` — reads `config.yml` and writes `index.html`. Edit `config.yml`, then
  run `python build_page.py`.
- `index.html` — the generated page, committed and served directly by GitHub Pages.

GitHub Pages serves `index.html` straight from the `main` branch (Settings → Pages →
Source: **Deploy from a branch**, `main` / root).

## Changing prices

1. Edit `config.yml` (prices, `site.tip-url`, effects).
2. Run `python build_page.py` to regenerate `index.html`.
3. Commit and push both files — Pages republishes the new `index.html` automatically.

The page lives at `https://a-quip.github.io/raidmayhem-donate-2/`. Put that URL in the
chatbot's `!donate` command.
