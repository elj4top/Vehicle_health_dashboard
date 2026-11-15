# Vehicle Health Dashboard

A Django web dashboard that turns a vehicle drive log into live-style readings, charts and plain-English findings. Part of a 5-project automotive diagnostics portfolio.

## What it does
- Reads a drive log in the same CSV format written by the OBD-II Diagnostic Analyzer (project 1)
- Shows current readings, an overall health status, and charts for engine speed, throttle, coolant temperature and fuel trims
- Analyzes trends across the whole drive, such as long term fuel trim climbing toward a lean condition, and links them to stored trouble codes

## Run it
    pip install -r requirements.txt
    python generate_sample_data.py
    python manage.py runserver

## Note on data
The included sample log is simulated: a 10-minute drive with a developing lean condition and a stored P0171 code. Real logs from the OBD-II Analyzer use the same format and can be dropped into the data folder.
