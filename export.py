from prometheus_client import start_http_server, Counter
import pyRAPL
import time

# TODO: fix this constant
KG_CARBON_PER_JOULE = 0.954  # EPA, 2018 ...


start_http_server(8000)

pkg_energy_gauge = Counter('pkg_energy', 'Cumulative energy consumed by CPU (J)')
pkg_carbon_eq_gauge = Counter('pkg_carbon_eq', 'Cumulative carbon emissions produced by CPU (kg)')

dram_energy_gauge = Counter('dram_energy', 'Cumulative energy consumed by DRAM (J)')
dram_carbon_eq_gauge = Counter('dram_carbon_eq', 'Cumulative carbon emissions produced by DRAM (kg)')

total_energy_gauge = Counter('total_energy', 'Cumulative energy consumed in total (J)')
total_carbon_eq_gauge = Counter('total_carbon_eq', 'Cumulative carbon emissions produced in total (kg)')

pyRAPL.setup()

meter = pyRAPL.Measurement('energy_meter')  # measures consumption of CPU and DRAM

while True:
    meter.begin()

    time.sleep(1.0)  # space out samples

    if meter.result is not None:
        pkg_energy_sample = sum(meter.result.pkg) / 10**6
        pkg_energy_gauge.inc(pkg_energy_sample)
        pkg_carbon_eq_gauge.inc(KG_CARBON_PER_JOULE * pkg_energy_sample)

        dram_energy_sample = sum(meter.result.dram) / 10 ** 6
        dram_energy_gauge.inc(dram_energy_sample)
        dram_carbon_eq_gauge.inc(KG_CARBON_PER_JOULE * dram_energy_sample)

        total_energy_sample = pkg_energy_sample + dram_energy_sample
        total_energy_gauge.inc(total_energy_sample)
        total_carbon_eq_gauge.inc(KG_CARBON_PER_JOULE * total_energy_sample)

    meter.end()
