#!/usr/bin/env python3
"""
Generates index.html from this repo's config.yml.

This is a standalone donate page: prices, tip URL, and effects all come from the
sibling config.yml. Edit config.yml, then re-run.

Run locally:   python build_page.py
CI runs it on every push (see .github/workflows/deploy.yml).
"""
from pathlib import Path
from urllib.parse import urlparse
import html
import yaml

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "config.yml"
OUT = HERE / "index.html"

# Fallbacks if the site: block leaves these out.
DEFAULT_TIP_URL = "https://streamelements.com/your_channel/tip"


def pretty(name: str) -> str:
    return name.replace("_", " ").title()


def money(v: float) -> str:
    return f"${v:,.2f}"


def channel_from(url: str) -> str:
    """The streamer's tag — the first path segment of the tip URL."""
    parts = [p for p in urlparse(url).path.split("/") if p]
    return parts[0] if parts else "the stream"


def load():
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
    site = cfg.get("site") or {}
    return dict(
        tip_url=site.get("tip-url") or DEFAULT_TIP_URL,
        effects=site.get("effects") or {},          # name -> description
        effect_costs=cfg.get("effects") or {},      # name -> minimum tip
        mobs=cfg.get("mob-whitelist") or {},
        items=(cfg.get("gifts") or {}).get("whitelist") or {},
        mob_cap=(cfg.get("mobs") or {}).get("max-per-donation", 256),
        gift_cap=(cfg.get("gifts") or {}).get("max-per-donation", 512),
    )


def priced_rows(catalog: dict, kind: str) -> str:
    def cost_of(v):
        # Match the plugin: a blank / non-numeric cost falls back to 1.0.
        return float(v) if isinstance(v, (int, float)) else 1.0
    rows = []
    for name, cost in sorted(catalog.items(), key=lambda kv: (cost_of(kv[1]), kv[0])):
        marker = f"{kind}:{name}"
        rows.append(
            f'<tr><td>{html.escape(pretty(name))}</td>'
            f'<td><code>{html.escape(marker)}</code></td>'
            f'<td class="num">{money(cost_of(cost))}</td></tr>'
        )
    return "\n  ".join(rows)


def effect_price(cost) -> str:
    """Effects cost a minimum tip (the effects: map); 0/absent means any tip works."""
    return money(float(cost)) if isinstance(cost, (int, float)) and cost > 0 else "any tip"


def effect_rows(effects: dict, costs: dict) -> str:
    rows = []
    for name, desc in effects.items():
        rows.append(
            f'<tr><td>{html.escape(pretty(name))}</td>'
            f'<td><code>EFFECT:{html.escape(name)}</code></td>'
            f'<td>{html.escape(str(desc))}</td>'
            f'<td class="num">{effect_price(costs.get(name))}</td></tr>'
        )
    return "\n  ".join(rows)


def build() -> str:
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Donate - {channel}</title>
<style>
  body{{font-family:Arial,Helvetica,sans-serif;max-width:720px;margin:0 auto;
    padding:18px;color:#111;line-height:1.5}}
  h1{{font-size:24px;margin:0 0 10px}}
  h2{{font-size:17px;margin:24px 0 6px}}
  a.donate{{display:inline-block;background:#2e7d32;color:#fff;text-decoration:none;
    padding:9px 18px;border-radius:4px;font-weight:bold}}
  a.donate:hover{{background:#276b2b}}
  table{{border-collapse:collapse;width:100%}}
  th,td{{border:1px solid #ccc;padding:5px 9px;text-align:left;font-size:14px}}
  th{{background:#f0f0f0}}
  td.num{{text-align:right;white-space:nowrap}}
  code{{background:#f4f4f4;padding:1px 4px;font-size:13px}}
</style>
</head>
<body>
  <h1>Donate to {channel}'s stream</h1>
  <a class="donate" href="{tip}">Donate here</a>

  <h2>How to donate</h2>
  <p>Put a marker in your tip message to choose what to send. The amount sets how many
  (count = amount divided by the price), up to {mob_cap} mobs or {gift_cap} items per tip.
  Only the first marker in a message counts, so it's one effect per tip; an effect needs a
  tip of at least its listed price and then fires once (tipping more does nothing extra).
  Prices are set by the streamer and may change.</p>
  <p>Examples:<br>
  <code>MOB:Enderman</code> sends endermen<br>
  <code>ITEM:Diamond</code> sends diamonds (multi-word names use an underscore, like ITEM:golden_apple)<br>
  <code>EFFECT:Heal</code> heals all runners<br>
  Add <code>IGN:YourName</code> to control the mob you send.</p>

  <h2>Mobs (MOB:name)</h2>
  <table>
  <tr><th>Mob</th><th>Marker</th><th>Each</th></tr>
  {mob_rows}
  </table>

  <h2>Items (ITEM:name)</h2>
  <table>
  <tr><th>Item</th><th>Marker</th><th>Each</th></tr>
  {item_rows}
  </table>

  <h2>Effects (EFFECT:name)</h2>
  <table>
  <tr><th>Effect</th><th>Marker</th><th>Does</th><th>Price</th></tr>
  {effect_rows}
  </table>
</body>
</html>
"""


def main():
    data = load()
    page = build().format(
        tip=html.escape(data["tip_url"]),
        channel=html.escape(channel_from(data["tip_url"])),
        mob_rows=priced_rows(data["mobs"], "MOB"),
        item_rows=priced_rows(data["items"], "ITEM"),
        effect_rows=effect_rows(data["effects"], data["effect_costs"]),
        mob_cap=data["mob_cap"],
        gift_cap=data["gift_cap"],
    )
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} - {len(data['mobs'])} mobs, {len(data['items'])} items, "
          f"{len(data['effects'])} effects")


if __name__ == "__main__":
    main()
