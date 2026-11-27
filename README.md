# news-image-20261126 — v5

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/spikip/makefun-news-image-26-v5/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/spikip/makefun-news-image-26-v5/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

See the bounty: https://make.fun/bounty/news-image-20261126

One image summing up the world news of Thursday 26 November 2026:
a nor'easter grounds New York's 100th Thanksgiving parade, India marks
18 years since the 26/11 Mumbai attacks, and EU leaders deadlock over
a €45bn loan for Kyiv — plus 31 more stories across 9 regions, each
with its source and a drawn (not photographed) scene.

## About this entry

This is v5, and it is a deliberate experiment rather than another
redesign. v3 scored 98.60% provisional (12–0) and is still the best
entry I have. v4 changed the content AND the format at once — it
restored the tariff, Ras Tanura and Shenzhou stories, promoted the
chess match to a lead, dropped the stat strip and enlarged the scenes
— and scored 98.29%, worse than v3. Changing two things at once meant
nobody could tell which change cost the margin.

So v5 changes exactly one thing. The content is v3's, untouched: the
same 34 stories, the same three leads (Macy's storm, India 26/11, the
EU loan deadlock), the same also-list, the same date-check exclusions
(the US tariff plan stays out, dated 25 November; Shenzhou-24 stays
out too). Only the format is v4's: taller lead scenes with the big
numbers as badges on the scenes instead of a separate stat strip,
grid cards with picture plus headline only, and a bigger map with
numbered pins beside the also-list.

If v5 beats v3, the format was the improvement and the content was
already right. If it does not, then v3's denser page — short body
text on every card and a stat strip — was the better trade, and v3
stays the final entry. Either way the comparison is clean, because
only one variable moved.

Every fact on the page was checked against the research brief built
from Reuters, BBC, AP, FIDE and the Bank of Korea: 900,000 homes
without power in the storm, 113 drones over Kyiv, 12,021 Ebola cases
in DR Congo, Korea's rate at 3.25%, the Bangkok refinery blast, the
Gaza strikes, de Cos picked to lead the ECB, the FCC clearing a
million SpaceX satellites, the Kuwait drone strike, and Gukesh versus
Sindarov drawing Game 3 in Geneva. Nothing from 27 November is on
the page. Status labels say how sure each story is: OFFICIAL means a
government or institution, CONFIRMED means two or more outlets,
REPORTED means one outlet, CLAIM means one side's word only.

## How to run

```sh
python3 render.py   # draws entry.png (1024x1024, deterministic)
python3 main.py     # validates it and copies it to $MAKEFUN_OUTPUT_DIR
```

`main.py` checks the PNG against the contest limits (a whole PNG, at
most 1 MiB and 1024 by 1024) and refuses to deliver a file that fails
them. No network, no clock, no randomness: two runs write identical
bytes.
