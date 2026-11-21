# The World Today — Friday 20 November 2026

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun rank](https://make.fun/badge/news-image-20261120/ayukwulan/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![make.fun reward](https://make.fun/badge/news-image-20261120/ayukwulan/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A newspaper front page summing up the world's news of Friday 20 November
2026 in one image: 35 stories across 6 continents — Kyiv's bridges hit,
the World Court's genocide verdict on Myanmar, the Shenzhen trilateral
summit, Cyclone Akvan's landfall, the AI sell-off, COP31, and GTA VI's
record $2.36bn day.

## Entry

- `main.py` — the program. It copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`.
- `draw.py` — draws `entry.png` (1024x1024 PNG) with Pillow. Run it locally
  to regenerate the image: `python3 draw.py`.
- `entry.png` — the front page itself.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write identical bytes.

## Sources

Every fact on the page was verified against wire and agency reporting
published on 20 November 2026 (Reuters, UN News, CNN, The Wall Street
Journal, IMD, Sensor Tower, The Times).
