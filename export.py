from prometheus_client import start_http_server, Gauge, Counter
from samplers import sample_avg_pkg_power, sample_avg_dram_power

# TODO: fix this constant
KG_CARBON_PER_KWH = 0.954  # from Emissions & Generation Resource Integrated Database (EPA, 2018)
PUE = 1.58  # Power Usage Effectiveness (PUE) from (Citation, 2019)

# Prometheus configuration
start_http_server(8000)

pkg_power_gauge = Gauge('avg_pkg_power', 'Sample average power drawn by CPU (W)')
pkg_carbon_eq_counter = Counter('pkg_carbon_eq', 'Cumulative carbon emissions produced by CPU (kg)')

dram_power_gauge = Gauge('avg_dram_power', 'Sample average power drawn by DRAM (W)')
dram_carbon_eq_counter = Counter('dram_carbon_eq', 'Cumulative carbon emissions produced by DRAM (kg)')

total_power_gauge = Gauge('avg_total_power', 'Sample average total power drawn (W)')
total_carbon_eq_counter = Counter('total_carbon_eq', 'Cumulative carbon emissions produced in total (kg)')

# Sample power drawn by CPU and DRAM
while True:
    pkg_power_sample = sample_avg_pkg_power(10, 0.01)
    pkg_power_gauge.set(pkg_power_sample)
    pkg_carbon_eq_counter.inc(KG_CARBON_PER_KWH * pkg_power_sample)

    dram_power_sample = sample_avg_dram_power(10, 0.01)
    dram_power_gauge.set(dram_power_sample)
    dram_carbon_eq_counter.inc(KG_CARBON_PER_KWH * dram_power_sample)

    total_power_sample = pkg_power_sample + dram_power_sample
    total_power_gauge.set(total_power_sample)
    total_carbon_eq_counter.inc(KG_CARBON_PER_KWH * total_power_sample)
