from pathlib import Path
from django.conf import settings
from django.shortcuts import render
from .analysis import load_log, analyze, overall_status

DATA_FILE = Path(settings.BASE_DIR) / "data" / "sample_drive.csv"

def dashboard(request):
    rows = load_log(DATA_FILE)
    findings = analyze(rows)
    latest = rows[-1] if rows else {}
    status = overall_status(findings)
    chart_data = {
        "labels": [r["timestamp"][11:19] for r in rows],     # HH:MM:SS
        "rpm": [r["RPM"] for r in rows],
        "throttle": [r["THROTTLE_POS"] for r in rows],
        "coolant": [r["COOLANT_TEMP"] for r in rows],
        "stft": [r["SHORT_FUEL_TRIM_1"] for r in rows],
        "ltft": [r["LONG_FUEL_TRIM_1"] for r in rows],
    }
    return render(request, "health/dashboard.html", {
        "status": status,
        "status_class": status.split()[0],
        "findings": findings,
        "latest": latest,
        "sample_count": len(rows),
        "chart_data": chart_data,
    })
