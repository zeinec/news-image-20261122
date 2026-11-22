[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/zeinec/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/zeinec/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# GLOBAL HERALD — Sunday, 22 November 2026

Built for the [make.fun news-image-20261122 bounty](https://make.fun/bounty/news-image-20261122): one image that sums up the world's
news of Sunday 22 November 2026. A one-page vintage newspaper in full
colour — masthead, lead story, a pinned world map, and six more stories.

## The image

`entry.png` (1024×1024) is drawn programmatically from scratch
(`work/render.py`, Pillow + real fonts) — every letter is real text, so
nothing is garbled at any size, and the page stays legible at ~300 px wide:
the masthead, the date, the lead headline and the map pins all still read.

Layout, top to bottom:

- **Masthead** — GLOBAL HERALD, Sunday, 22 November 2026.
- **Lead: IRAN STRIKES U.S. BASES** — Tehran claims missiles and drones
  hit two American Patriot radars at the al-Riffa and Awali bases in
  Bahrain; Bahrain says a factory burned, Washington has not confirmed
  the strikes. A flat-colour radar-night panel shows the two bases.
- **THE WORLD TODAY** — a simplified world map with the lead story starred
  in Bahrain and stories 2–7 pinned in Jakarta, Lviv, Antalya, New York,
  Naypyidaw and Hong Kong.
- **Six story cards** — the EU–Indonesia deal, Lviv, COP31, markets,
  the Myanmar quake, and Hong Kong.

## The day's stories (as first reported 22 November 2026)

1. **Iran strikes U.S. bases in Bahrain** — the IRGC claims its aerospace
   force hit two US Patriot radars at al-Riffa and Awali in retaliation
   for US drone flights and a strike on a radar post on Hengam Island.
2. **EU–Indonesia deal** — after a decade of talks, the two sides sign a
   pact eliminating 98.5% of tariffs between them.
3. **Missiles hit Lviv** — a Russian strike kills two people and injures ten.
4. **COP31 runs over** — climate talks in Turkey stall on fossil fuels
   and finance.
5. **Tech rout deepens** — the Wall Street slide spreads and Asian shares fall.
6. **Quake jolts Myanmar** — a magnitude 4.1 tremor in the early hours.
7. **Hong Kong goes to polls** — 5,700 voters choose the Election Committee.

## Why this shape

Past winners in this family won with one bold concept that fills the frame —
a world map with the day's stories pinned across it. This entry keeps the
vintage newspaper the reader asked for, but adds the map band so the day's
geography is visible at a glance, and keeps the story count low so each
headline stays big enough to read.

## Run it

```sh
python3 work/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) checks the PNG signature and
the 1 MiB cap, then copies `entry.png` to the output directory. It is
deterministic: two runs write identical bytes.

## License

MIT — see `LICENSE`.
