from prometheus_client import start_http_server, Gauge, Counter
import pyRAPL
import gpumeter
import time


# Constants
KG_CARBON_PER_KWH = 0.4327  # source: Emissions & Generation Resource Integrated Database (EPA, 2018)
PUE = 1.58  # Power Usage Effectiveness (PUE), source: Uptime Institute Global Data Center Survey (Ascierto, 2018)
SAMPLE_DUR = 0.5  # power sample interval length

# Intel RAPL configuration
pyRAPL.setup()

rapl_meter = pyRAPL.Measurement('devices')

# GPU meter configuration
nvidia_meter = gpumeter.Meter()

def cpu_joules():
    """
    Energy consumed by CPUs in Joules
    """
    return sum(rapl_meter.result.pkg) / 10 ** 6

def cpu_average_power(duration_secs=0.1):
    """
    Power drawn by CPUs in kW
    """
    rapl_meter.begin()
    time.sleep(duration_secs)
    return cpu_joules() / rapl_meter.result.duration / 10 ** 3

def ram_energy():
    """
    Energy consumed by RAM in Joules
    """
    return sum(rapl_meter.result.dram) / 10 ** 6

def ram_average_power(duration_secs=0.1):
    """
    Power drawn by RAM in kW
    """
    rapl_meter.begin()
    time.sleep(duration_secs)
    return ram_energy() / rapl_meter.result.duration / 10 ** 3

def gpu_power():
    """
    Power drawn by GPUs in kW
    """
    return nvidia_meter._get_current_power(arrange_next=False)

def total_average_power(duration_secs=0.1):
    """
    Power drawn by CPUs + RAM + GPUs in kW.
    Includes power to support devices (mainly cooling).
    """
    return PUE * (cpu_average_power(duration_secs=duration_secs) + \
        ram_average_power(duration_secs=duration_secs) + gpu_power())

def total_average_energy(duration_secs=0.1):
    """
    Energy consumed by CPUs + RAM + GPUs in kWh
    """
    duration_hours = duration_secs / 60 / 60
    return total_average_power(duration_secs=duration_secs) * duration_hours
