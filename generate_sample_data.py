import csv
import math
import os
import random
from datetime import datetime, timedelta

random.seed(7)  # same data every run, so results are repeatable

os.makedirs("data", exist_ok=True)
start = datetime(2026, 11, 14, 9, 0, 0)
HEADER = ["timestamp", "RPM", "COOLANT_TEMP", "SHORT_FUEL_TRIM_1",
          "LONG_FUEL_TRIM_1", "THROTTLE_POS", "dtcs"]

coolant = 30.0
rows = []
for i in range(300):                       # 300 samples, one every 2 seconds = 10 minutes
    t = start + timedelta(seconds=2 * i)
    phase = i / 299                        # 0 -> 1 over the drive
    effort = math.sin(phase * math.pi) ** 2   # idle -> hard driving -> back to idle

    rpm = 850 + 1800 * effort + random.gauss(0, 40)
    throttle = 12 + 35 * effort + random.gauss(0, 1.5)
    coolant = min(92.0, coolant + 0.35 + random.gauss(0, 0.05))   # engine warming up
    ltft = 1.0 + 11.0 * phase + random.gauss(0, 0.4)              # creeping positive: lean condition developing
    stft = 2.0 + (ltft - 6) * 0.1 + random.gauss(0, 1.8)
    dtcs = "P0171" if i >= 210 else ""     # code gets stored late in the drive

    rows.append([t.isoformat(), round(rpm), round(coolant, 1), round(stft, 1),
                 round(ltft, 1), round(throttle, 1), dtcs])

with open("data/sample_drive.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)
    writer.writerows(rows)

print(f"Wrote {len(rows)} readings to data/sample_drive.csv")
