# antigravity-usage-tracker

Small CLI for reading Antigravity logs and showing when quota opens again.
The executable is `ag`.

This repository is code-only. Local tracker state, personal logs, and machine-specific data are intentionally not committed.

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
