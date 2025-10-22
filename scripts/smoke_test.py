import logging
import sys
from collections import Counter
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from adapters.audio.ai_mode_detector import AiAudioModeDetector
from adapters.audio.wav_reader import ZipWavFileReader
from adapters.filesystem.file_discovery import discover_and_pair_files
from core.domain.comparison import compare_data
from config import cfg
from pdf_extractor import extract_pdf_tracklist
from ui.config_models import load_id_extraction_settings, load_tolerance_settings

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

pdf_dir = Path('test_data/pdf').resolve()
wav_dir = Path('test_data/wav').resolve()
print(f"Using pdf_dir={pdf_dir}")
print(f"Using wav_dir={wav_dir}")

if not pdf_dir.exists() or not wav_dir.exists():
    print("Test data directories not found. Aborting.")
    sys.exit(2)

tolerance_settings = load_tolerance_settings(cfg)
id_extraction_settings = load_id_extraction_settings(cfg)
wav_reader = ZipWavFileReader()
audio_mode_detector = AiAudioModeDetector()

pairs, skipped = discover_and_pair_files(pdf_dir, wav_dir, id_extraction_settings)
print(f"Found {len(pairs)} pair(s); {skipped} ambiguous skipped")

all_results = []
for i, (file_id, pair_info) in enumerate(pairs.items(), 1):
    print(f"Processing {i}/{len(pairs)}: {pair_info['pdf'].name}")
    pdf_data = extract_pdf_tracklist(pair_info['pdf'])
    wav_data = wav_reader.read_wav_files(pair_info['zip'])
    side_results = compare_data(pdf_data, wav_data, pair_info, tolerance_settings, audio_mode_detector)
    all_results.extend(side_results)

print(f"Side results: {len(all_results)}")
# Print brief summary
status_counts = Counter(r.status for r in all_results)
print("Status counts:", dict(status_counts))

# Exit code 0 if at least one result, else 1
sys.exit(0 if all_results else 1)
