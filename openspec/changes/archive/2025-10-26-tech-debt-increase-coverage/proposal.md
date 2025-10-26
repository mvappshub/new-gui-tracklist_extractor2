# Proposal: tech-debt-increase-coverage

### 1. Reasoning
During the finalization of `fix-waveform-port-integration`, the coverage gate failed (78% < 85%). To unblock the change, the threshold was temporarily lowered to 78%.

This change is dedicated to addressing this technical debt by increasing test coverage back to the required 85% threshold and restoring the original value in `tools/check.sh`.
