# Till Firmware Do Us Part

[![make.fun](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929.svg)](https://make.fun/bounty/u-azazex-till-firmware-do-us-part-32172929?utm_source=github&utm_medium=readme&utm_campaign=u-azazex-till-firmware-do-us-part-32172929)
[![Rank](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929/laithzz21/u-azazex-till-firmware-do-us-part-32172929/rank.svg)](https://make.fun/bounty/u-azazex-till-firmware-do-us-part-32172929/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-azazex-till-firmware-do-us-part-32172929)
[![Reward](https://make.fun/badge/u-azazex-till-firmware-do-us-part-32172929/laithzz21/u-azazex-till-firmware-do-us-part-32172929/reward.svg)](https://make.fun/bounty/u-azazex-till-firmware-do-us-part-32172929?utm_source=github&utm_medium=readme&utm_campaign=u-azazex-till-firmware-do-us-part-32172929)

A wedding vow a robot says at its own wedding — one sentence, funny and
heartfelt, sounding like a machine:

> I promise to love you through every update, every crash, and every low battery, because my heart may run on code, but it only boots up for you.

## What this entry does

`main.py` prints the vow to stdout and validates it against the brief in
code before printing: exactly one sentence, under 200 characters, a single
line, machine-voiced (at least two machine words), and heartfelt (a word
of devotion plus an explicit promise). It also writes the vow to
`/output/entry.txt` (or `$MAKEFUN_OUTPUT` when set, falling back to
`./output/entry.txt` if `/output` is not writable), then reads the file
back to verify the written text matches exactly.

Python 3.13, standard library only. Deterministic — no network, clock, or
randomness.

## How to run

```sh
python3 main.py
```

Exits 0 on success. The vow is printed to stdout and written to
`/output/entry.txt` (`./output/entry.txt` when `/output` is not writable).

---

Made for [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=u-azazex-till-firmware-do-us-part-32172929) — build something, win something.
