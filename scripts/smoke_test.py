from collections import Counter
import sys
import logging
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from adapters.filesystem.file_discovery import discover_and_pair_files
from pdf_extractor import extract_pdf_tracklist
from core.domain.extraction import extract_wav_durations_sf
from core.domain.comparison import compare_data

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

pdf_dir = Path('test_data/pdf').resolve()
wav_dir = Path('test_data/wav').resolve()
print(f"Using pdf_dir={pdf_dir}")
print(f"Using wav_dir={wav_dir}")

if not pdf_dir.exists() or not wav_dir.exists():
    print("Test data directories not found. Aborting.")
    sys.exit(2)

pairs, skipped = discover_and_pair_files(pdf_dir, wav_dir)
print(f"Found {len(pairs)} pair(s); {skipped} ambiguous skipped")

all_results = []
for i, (file_id, pair_info) in enumerate(pairs.items(), 1):
    print(f"Processing {i}/{len(pairs)}: {pair_info['pdf'].name}")
    pdf_data = extract_pdf_tracklist(pair_info['pdf'])
    wav_data = extract_wav_durations_sf(pair_info['zip'])
    side_results = compare_data(pdf_data, wav_data, pair_info)
    all_results.extend(side_results)

print(f"Side results: {len(all_results)}")
# Print brief summary
status_counts = Counter(r.status for r in all_results)
print("Status counts:", dict(status_counts))

# Exit code 0 if at least one result, else 1
sys.exit(0 if all_results else 1)

