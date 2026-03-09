# 2026 Retrospective: Discord Transcription Stack

This is a "one year later" technical review of the current pipeline with practical upgrades that should give the biggest reliability and maintainability wins for the least effort.

## What still looks strong

- **Clean phase separation**: capture, audit, transcription, and transcript dedupe are clearly separated into scripts with predictable hand-offs via JSONL.
- **Useful audit semantics**: `dedupe_audit.py` captures rejection reasons (`rms_silent`, `vad_reject_short`, `sha256_duplicate`, etc.), which makes threshold tuning practical.
- **Speaker-aware dedupe**: `dedupe_transcript.py` clusters per speaker, reducing cross-talk merge mistakes.
- **Operational pragmatism**: the burst-rescue path for short utterances is still a good idea for gaming/voice-chat cadence.

## High-value improvements (recommended order)

1. **Make VAD loading offline and reproducible**
   - Today `torch.hub.load(..., force_reload=True)` guarantees network calls and mutable upstream behavior.
   - Move to pinned local model assets (or at least disable force reload), and fail with a clear setup message if assets are missing.

2. **Fix `index.ts` compile/runtime sharp edges**
   - The static `userNames` map currently includes an extra trailing comma entry that breaks TypeScript parsing.
   - There is also a `streamCount` decrement in both the pipeline callback and a timeout fallback, which can double-decrement and drift negative.

3. **Preserve non-accepted rows during transcription step**
   - `transcribe_accepted.py` currently writes only accepted entries to output, dropping rejected items and reducing audit traceability.
   - Better pattern: keep full list, enrich accepted rows with `text`, and write all rows back out.

4. **Add deterministic environment pinning**
   - Add exact package pins and a small `requirements-lock.txt` or constraints file.
   - Document CUDA/CT2 matrix known-good combinations for future rebuilds.

5. **Add a tiny fixture-based regression test set**
   - A few representative JSONL/audio stubs to test dedupe clustering, containment filtering, and burst rescue logic will prevent accidental behavior drift.

## Modernization ideas (nice-to-have)

- **Optional diarization/SAD upgrade path** for multi-speaker overlap and cleaner segment boundaries.
- **Post-processing pass** for punctuation/casing normalization before clustering to reduce near-duplicate miss rate.
- **Run metadata manifest** per session (model hash, commit SHA, thresholds), useful for reproducibility when comparing transcripts.

## Quick confidence checklist for a fresh machine

- `index.ts` builds cleanly with current Node + TypeScript toolchain.
- VAD model can be resolved without internet.
- A known sample session runs end-to-end producing:
  - audit JSONL,
  - transcribed JSONL,
  - final deduped transcript.
- Summary counts are stable across two consecutive runs on same inputs.

## Bottom line

The core architecture still holds up well. If you only do three things now: **(1) VAD reproducibility**, **(2) `index.ts` hygiene fixes**, and **(3) transcription output preservation**. Those will buy the biggest reduction in "future you" pain.
