# Tasks: lint-waveform-ruff

## 1. Preparation
- [ ] 1.1 Add `ruff==0.6.9` to `requirements.txt` (dev dependency acceptable in shared file for now)
- [ ] 1.2 Install dependencies in venv

## 2. Run Ruff & Fixes
- [ ] 2.1 Run `ruff check ui/waveform`
- [ ] 2.2 Apply minimal, behavior-neutral fixes in `ui/waveform/*`
- [ ] 2.3 Re-run `ruff check ui/waveform` until clean

## 3. Validation
- [ ] 3.1 `openspec validate lint-waveform-ruff --strict`
- [ ] 3.2 `pytest -q`
- [ ] 3.3 `mypy --strict`

## 4. Commit & PR
- [ ] 4.1 Commit: `chore(ruff): lint ui/waveform with ruff [refs: #openspec-task:1]`
- [ ] 4.2 Open PR; gates: OpenSpec, Pytest, Mypy

## Notes
- Limit scope to `ui/waveform/` only (waveform-utils, plot controller, playback controller, audio loader)
- No test modifications beyond formatting; no behavior changes
