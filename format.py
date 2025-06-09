import os
import csv
from pathlib import Path

# GitHub raw URL prefix pointing directly to tts_outputs
GITHUB_PREFIX = "https://github.com/nukkk97/spear_long/raw/refs/heads/main/tts_outputs"
BASE_DIR = Path("tts_outputs")
OUTPUT_FILE = "output.csv"

def generate_csv():
    rows = []
    subdirs = sorted([d for d in BASE_DIR.iterdir() if d.is_dir()])

    for idx, subdir in enumerate(subdirs):
        wav_files = sorted(subdir.glob("*.wav"))
        if len(wav_files) == 2:
            audio1 = f"{GITHUB_PREFIX}/{subdir.name}/{wav_files[0].name}"
            audio2 = f"{GITHUB_PREFIX}/{subdir.name}/{wav_files[1].name}"
            rows.append([idx, audio1, audio2])
        else:
            print(f"Skipping {subdir.name} — expected 2 .wav files, found {len(wav_files)}")

    # Write to CSV
    with open(OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "audio1", "audio2"])
        writer.writerows(rows)

    print(f"CSV written to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_csv()
