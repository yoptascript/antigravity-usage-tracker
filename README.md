# antigravity-usage-tracker

Small CLI for reading Antigravity logs and showing when quota opens again.
The executable is `ag`.

This repository is code-only. Local tracker state, personal logs, and machine-specific data are intentionally not committed.

## Quick install

Copy and paste this into your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/yoptascript/antigravity-usage-tracker/main/install.sh | sh
```

The installer downloads `ag`, installs it into a user bin directory, and runs `ag help` immediately.

## Commands

- `./ag next`: show the most recent detected quota exhaustion event and the next reset window
- `./ag watch`: watch Antigravity logs and print new exhaustion events as they appear
- `./ag help`: show command help

## Validation

```bash
python3 -m unittest tests/test_ag.py
./ag help
./ag next
```
