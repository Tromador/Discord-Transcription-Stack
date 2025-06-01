# Discord Audio Transcript Deduplication Pipeline

This repository contains a multi-stage pipeline for processing, transcribing, and deduplicating Discord voice session recordings into clean text transcripts. It includes tools for audio capture, filtering, transcription, clustering-based deduplication, and final text output.

## 📚 Overview

The pipeline operates in the following phases:
1. **Phase 0** – **Discord Audio Capture**  
   Captures user audio streams as individual `.wav` files and generates session logs.

2. **Phase 1** – **Audio Validation and Filtering**  
   Filters audio for silence, duration constraints, and rescues bursty utterances with VAD.

3. **Phase 2** – **Whisper Transcription**  
   Transcribes accepted audio files to text using a CTranslate2-based Whisper model.

4. **Phase 3** – **Deduplication by Clustering**  
   Clusters transcriptions and deduplicates based on similarity, canonical form, and scoring.

5. **Output** – A cleaned `.txt` transcript preserving character, flow, and session integrity.

## 🛠 Scripts

| Script                  | Purpose                                                   |
|--------------------------|-----------------------------------------------------------|
| `index.ts`               | Captures Discord voice as per-user `.wav` files          |
| `dedupe_audit.py`        | Filters raw audio: silence, noise, duplicates, duration   |
| `burst_scope.py`         | Rescues short sharp utterances from false VAD rejection   |
| `transcribe_accepted.py` | Transcribes accepted `.wav` files into enriched JSONL     |
| `dedupe_transcript.py`   | Deduplicates transcribed JSONL using clustering           |

## 🚀 Quick Start

1. Clone the repo and install required Python and Node.js dependencies.
2. Configure `.env` with your Discord bot credentials.
3. Run each phase in sequence:
   - `index.ts` to capture audio.
   - `dedupe_audit.py` to filter audio.
   - `transcribe_accepted.py` to transcribe.
   - `dedupe_transcript.py` to deduplicate.
4. Review the final transcript output.

---

## ⚡ Key Notes
- Built specifically for **GPU-accelerated transcription** with **faster-whisper**.
- Designed and tested on a **GeForce RTX 5090** with a custom-built **CTranslate2** backend.
- Provided **"as is"**, with no guarantees; it's up to you to configure and compile any needed dependencies.

---

## 📦 Installation

### Python Dependencies
    pip install -r requirements.txt
(further dependencies may be required)

### Node.js Dependencies
    npm install 
(further dependencies may be required)

---

## 📜 License
BSD 3-Clause License — Permissive use, with **attribution required**.  

---
