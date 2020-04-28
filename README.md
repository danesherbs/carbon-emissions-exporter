# Carbon emissions exporter
A simple Python package that:
- Calculates physical quantities of your device `meters.py`
- Calculates useful metrics `metrics.py`

Also includes a server that exports these via HTTP for Prometheus consumption `export.py`

## Features

### Physical quantities
- Power (kW)
- Energy (kWh)
- CO2e emissions (kg)

### Metrics
- Donation to offset carbon emissions (USD)
- Number of one-way flights from London to New York

### Devices monitored
- CPU
- DRAM
- GPU

## Setup

### Use as a library
```python
import meters
import metrics
```
### Start server for Prometheus
```bash
python export.py
```

