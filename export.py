from prometheus_client import start_http_server, Gauge, Counter
import pyRAPL
import time


# TODO: fix this constant
KG_CARBON_PER_KWH = 0.954  # from Emissions & Generation Resource Integrated Database (EPA, 2018)
PUE = 1.58  # Power Usage Effectiveness (PUE) from (Citation, 2019)
SAMPLE_DELTA = 0.5  # seconds between samples

# Prometheus configuration
start_http_server(8000)

pkg_power_gauge = Gauge('avg_pkg_power', 'Sample average power drawn by CPU (W)')
pkg_carbon_eq_counter = Counter('pkg_carbon_eq', 'Cumulative carbon emissions produced by CPU (kg)')

dram_power_gauge = Gauge('avg_dram_power', 'Sample average power drawn by DRAM (W)')
dram_carbon_eq_counter = Counter('dram_carbon_eq', 'Cumulative carbon emissions produced by DRAM (kg)')

total_power_gauge = Gauge('avg_total_power', 'Sample average total power drawn (W)')
total_carbon_eq_counter = Counter('total_carbon_eq', 'Cumulative carbon emissions produced in total (kg)')

# Intel RAPL configuration
pyRAPL.setup()

meter = pyRAPL.Measurement('devices')

# Sample power drawn by CPU and DRAM
while True:
    meter.begin()
    time.sleep(SAMPLE_DELTA)  # space out samples
    meter.end()

    pkg_energy = sum(meter.result.pkg) / 10 ** 6
    pkg_avg_power = pkg_energy / meter.result.duration
    pkg_power_gauge.set(pkg_avg_power)
    pkg_carbon_eq_counter.inc(KG_CARBON_PER_KWH * pkg_avg_power)

    dram_energy = sum(meter.result.dram) / 10 ** 6
    dram_avg_power = dram_energy / meter.result.duration
    dram_power_gauge.set(dram_avg_power)
    dram_carbon_eq_counter.inc(KG_CARBON_PER_KWH * dram_avg_power)

    total_avg_power = pkg_avg_power + dram_avg_power
    total_power_gauge.set(total_avg_power)
    total_carbon_eq_counter.inc(KG_CARBON_PER_KWH * total_avg_power)