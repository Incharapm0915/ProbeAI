"""storage.py — Save candidate data locally as JSON"""
import json, os
from datetime import datetime

DATA_DIR = "probeai_data"


def save_candidate(candidate: dict, answers: list):
    os.makedirs(DATA_DIR, exist_ok=True)
    record = {
        "timestamp": datetime.now().isoformat(),
        "candidate": candidate,
        "answers":   answers,
    }
    fname = f"{DATA_DIR}/{candidate.get('name','unknown').replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w") as f:
        json.dump(record, f, indent=2)