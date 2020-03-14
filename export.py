from prometheus_client import start_http_server, Gauge, Counter
import pyRAPL
import gpumeter
import time


# Constants
KG_CARBON_PER_KWH = 0.4327  # source: Emissions & Generation Resource Integrated Database (EPA, 2018)
PUE = 1.58  # Power Usage Effectiveness (PUE), source: Uptime Institute Global Data Center Survey (Ascierto, 2018)
SAMPLE_DUR = 0.5  # power sample interval length

# Prometheus configuration
start_http_server(8000)

pkg_power_gauge = Gauge('avg_pkg_power', 'Sample average power drawn by CPU (kW)')
pkg_energy_counter = Counter('pkg_energy', 'Cumulative energy consumed by CPU (kWh)')
pkg_carbon_eq_counter = Counter('pkg_carbon_eq', 'Cumulative carbon emissions emitted powering CPU (kg)')

dram_power_gauge = Gauge('avg_dram_power', 'Sample average power drawn by DRAM (kW)')
dram_energy_counter = Counter('dram_energy', 'Cumulative energy consumed by DRAM (kWh)')
dram_carbon_eq_counter = Counter('dram_carbon_eq', 'Cumulative carbon emissions emitted powering DRAM (kg)')

gpu_power_gauge = Gauge('avg_gpu_power', 'Sample average power drawn by GPUs (kW)')
gpu_energy_counter = Counter('gpu_energy', 'Cumulative energy consumed by GPU (kWh)')
gpu_carbon_eq_counter = Counter('gpu_carbon_eq', 'Cumulative carbon emissions emitted powering GPUs (kg)')

total_power_gauge = Gauge('avg_total_power', 'Sample average total power drawn (kW)')
total_energy_counter = Counter('total_energy', 'Cumulative energy consumed in total (kWh)')
total_carbon_eq_counter = Counter('total_carbon_eq', 'Cumulative carbon emissions emitted in total (kg)')

# Intel RAPL configuration
pyRAPL.setup()

rapl_meter = pyRAPL.Measurement('devices')

# GPU meter configuration
nvidia_meter = gpumeter.Meter(1.0)

# Sample power drawn by CPU, DRAM and GPU
while True:
    rapl_meter.begin()

    time.sleep(SAMPLE_DUR)  # sample over some time

    if rapl_meter.result is not None:
        duration_hours = rapl_meter.result.duration / 60 / 60  # original duration is in seconds

        # CPU
        pkg_energy = sum(rapl_meter.result.pkg) / 10 ** 6  # Joules
        pkg_avg_power = pkg_energy / rapl_meter.result.duration / 10 ** 3  # kW
        pkg_energy_counter.inc(pkg_avg_power * duration_hours)
        pkg_power_gauge.set(pkg_avg_power)
        pkg_carbon_eq_counter.inc(KG_CARBON_PER_KWH * pkg_avg_power * duration_hours)

        # DRAM
        dram_energy = sum(rapl_meter.result.dram) / 10 ** 6  # Joules
        dram_avg_power = dram_energy / rapl_meter.result.duration / 10 ** 3  # kW
        dram_energy_counter.inc(dram_avg_power * duration_hours)
        dram_power_gauge.set(dram_avg_power)
        dram_carbon_eq_counter.inc(KG_CARBON_PER_KWH * dram_avg_power * duration_hours)

        # GPU
        gpu_avg_power = nvidia_meter._get_current_power(arrange_next=False)  # kW
        gpu_energy_counter.inc(gpu_avg_power * duration_hours)
        gpu_power_gauge.set(gpu_avg_power)
        gpu_carbon_eq_counter.inc(KG_CARBON_PER_KWH * gpu_avg_power * duration_hours)

        # All devices, including power to support devices (mainly cooling)
        total_avg_power = PUE * (pkg_avg_power + dram_avg_power + gpu_avg_power)  # kW
        total_energy_counter.inc(total_avg_power * duration_hours)
        total_power_gauge.set(total_avg_power)
        total_carbon_eq_counter.inc(KG_CARBON_PER_KWH * total_avg_power * duration_hours)

    rapl_meter.end()
