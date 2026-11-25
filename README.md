# The World — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/xiaokai2013/makefun-news-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/xiaokai2013/makefun-news-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-image newspaper front page summing up the world's news of
Wednesday 25 November 2026, built for the make.fun bounty
`news-image-20261125`.

## The day in seven stories

1. **Colombia** — All hostages freed in a dawn raid on a Cartagena
   supermarket after a 17-hour siege; one captor killed.
2. **Space** — Shenzhou-24 launches with Pakistan's first astronaut,
   the first foreigner aboard China's Tiangong station.
3. **Middle East** — Houthis claim strikes on Riyadh's PIF tower and the
   Ras Tanura refinery; the Saudi-led coalition bombs Yemen in reply.
4. **Labour** — Bangladesh raises garment workers' minimum wage 36% to
   17,000 taka after weeks of protests; fresh clashes follow.
5. **Disaster** — Three bodies recovered from a flooded gold mine in
   West Java; 26 miners still trapped in a 100-metre shaft.
6. **Pacific** — Australia and Solomon Islands sign a treaty barring
   foreign military bases, with a A$740m support package.
7. **Europe** — Spain's Sánchez and Feijóo clash in a TV debate four
   days before Sunday's snap election.

## How it is made

`render.py` (Pillow) draws the 1024×1024 front page from `news.json`.
`main.py` (standard library only) copies the committed `entry.png` to
`/output/entry.png`, so the program runs twice with identical bytes in a
bare container with no network and no fonts.

## License

MIT — see `LICENSE`.
