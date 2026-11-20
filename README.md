# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Innamora69/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Innamora69/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026, drawn
as a newspaper front page: a lead strip on Anthropic's $2 trillion Nasdaq
debut and the AI-doubt sell-off (Nikkei −4.8%), plus a Houthi missile
hitting the Riyadh wealth-fund tower, the COP31 draft dropping the
fossil-fuel exit, Israeli troops crossing Gaza's Yellow Line, Kenya's last
Ebola patient going home — and an "also today" ticker with the UK–EU
youth-mobility deal, Bukele's third-term bid, the Senegal boat sinking,
US sanctions, the Pete Rose pardon, UK drones for Ukraine and Kyiv hit
by missiles.

## Files

- `draw.py` — draws `entry.png` (1024×1024, Pillow, no network, no
  randomness: same run, same bytes). Run `python3 draw.py`.
- `entry.png` — the image the entry ships.
- `main.ts` — entrypoint (Node 22, stdlib only): validates the PNG (whole
  file, ≤1 MiB, ≤1024×1024), copies it to `/output/entry.png` and
  verifies the copy byte for byte.

## Run it

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT (see LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w36tq042&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
