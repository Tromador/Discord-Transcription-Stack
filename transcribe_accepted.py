import argparse
import json
from pathlib import Path
from faster_whisper import WhisperModel
from tqdm import tqdm

def load_entries(jsonl_path):
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def save_jsonl(entries, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            json.dump(entry, f)
            f.write('\n')

def main():
    parser = argparse.ArgumentParser(description="Transcribe accepted entries and write to JSONL.")
    parser.add_argument('--input-log', type=Path, required=True, help="Path to deduped .jsonl log")
    parser.add_argument('--audio-dir', type=Path, required=True, help="Directory containing audio files")
    parser.add_argument('--model-dir', type=Path, required=True, help="Path to Whisper CT2 model")
    parser.add_argument('--output-jsonl', type=Path, required=True, help="Path to save updated JSONL with transcriptions")
    args = parser.parse_args()

    model = WhisperModel(
        str(args.model_dir.resolve()),
        compute_type="auto",
        cpu_threads=1
    )

    entries = load_entries(args.input_log)
    accepted = [e for e in entries if e.get("status") == "accepted"]

    print(f"📝 Transcribing {len(accepted)} accepted entries...")
    for entry in tqdm(accepted, desc="Transcribing"):
        audio_path = args.audio_dir / entry["filename"]
        if not audio_path.exists():
            print(f"⚠️ Missing: {entry['filename']}")
            continue

        try:
            segments, _ = model.transcribe(str(audio_path), beam_size=5)
            entry["text"] = " ".join([seg.text.strip() for seg in segments])
        except Exception as e:
            print(f"❌ Failed to transcribe {entry['filename']}: {e}")

    save_jsonl(accepted, args.output_jsonl)
    print(f"✅ Saved updated JSONL to: {args.output_jsonl}")

if __name__ == "__main__":
    main()
