import csv

SIGNALS = ["RPM", "COOLANT_TEMP", "SHORT_FUEL_TRIM_1", "LONG_FUEL_TRIM_1", "THROTTLE_POS"]

def load_log(path):
    """Read a log in the same format the OBD-II Analyzer's logger.py writes."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            reading = {"timestamp": row["timestamp"], "dtcs": row["dtcs"]}
            for name in SIGNALS:
                reading[name] = float(row[name]) if row[name] != "" else None
            rows.append(reading)
    return rows

def analyze(rows):
    """Turn raw readings into findings a person can act on."""
    findings = []
    if not rows:
        return [("info", "No data in this log yet.")]

    ltft = [r["LONG_FUEL_TRIM_1"] for r in rows if r["LONG_FUEL_TRIM_1"] is not None]
    coolant = [r["COOLANT_TEMP"] for r in rows if r["COOLANT_TEMP"] is not None]
    codes = sorted({c for r in rows for c in r["dtcs"].split(";") if c})

    if ltft:
        start_avg = sum(ltft[:20]) / len(ltft[:20])
        end_avg = sum(ltft[-20:]) / len(ltft[-20:])
        if end_avg > 10:
            findings.append(("bad", f"Long term fuel trim ended at +{end_avg:.1f}%: the engine is "
                                    f"running lean and the ECU is adding a lot of fuel to compensate."))
        elif end_avg - start_avg > 5:
            findings.append(("warn", f"Long term fuel trim climbed from {start_avg:.1f}% to "
                                     f"{end_avg:.1f}% during this drive. A lean condition may be developing."))
        elif end_avg < -10:
            findings.append(("bad", f"Long term fuel trim ended at {end_avg:.1f}%: the engine is running rich."))

    if coolant:
        if max(coolant) > 110:
            findings.append(("bad", f"Coolant reached {max(coolant):.0f} C. Possible overheating."))
        elif max(coolant) < 80 and len(coolant) > 200:
            findings.append(("warn", "Coolant never reached normal operating temperature. "
                                     "A thermostat stuck open is a common cause."))

    for code in codes:
        findings.append(("bad", f"Stored trouble code {code} appeared during this log."))
    if "P0171" in codes and ltft and ltft[-1] > 5:
        findings.append(("info", "P0171 is backed by the live data: check intake boots, vacuum lines "
                                 "and the manifold gasket first."))

    if not findings:
        findings.append(("good", "No anomalies found in this log."))
    return findings

def overall_status(findings):
    levels = [level for level, _ in findings]
    if "bad" in levels:
        return "ATTENTION NEEDED"
    if "warn" in levels:
        return "WATCH"
    return "HEALTHY"
