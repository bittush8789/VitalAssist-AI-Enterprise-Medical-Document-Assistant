import json
import os
from datetime import datetime

DATA_FILE = "processing_history.json"

def load_history():
    """Load all processing history from disk."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_record(record: dict):
    """Append a new processing record to history."""
    history = load_history()
    record["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_stats():
    """Return summary statistics from the history."""
    history = load_history()
    total = len(history)

    # Collect all diagnoses
    all_diagnoses = []
    all_medications = []
    all_agents_time = {"OCR": 0, "Summary": 0, "Diagnosis": 0, "Insurance": 0, "Coding": 0}
    monthly = {}

    for rec in history:
        # Diagnoses
        diag = rec.get("diagnosis", {})
        if isinstance(diag, dict):
            all_diagnoses.extend(diag.get("diagnosis", []))
            all_medications.extend(diag.get("medications", []))

        # Monthly count
        ts = rec.get("timestamp", "")
        if ts:
            month_key = ts[:7]  # "2026-05"
            monthly[month_key] = monthly.get(month_key, 0) + 1

    return {
        "total_reports": total,
        "all_diagnoses": all_diagnoses,
        "all_medications": all_medications,
        "monthly": monthly,
        "history": history
    }
