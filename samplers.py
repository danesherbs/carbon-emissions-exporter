import pyRAPL
import time


def sample_avg_pkg_power(n_samples, sample_dur_secs):
    meter = pyRAPL.Measurement('energy')

    cum_avg_pkg_power = 0.0

    for _ in range(n_samples):
        meter.begin()
        time.sleep(sample_dur_secs)
        meter.end()

        pkg_energy = sum(meter.result.pkg) / 10**6
        avg_pkg_power = pkg_energy / meter.result.duration
        cum_avg_pkg_power += avg_pkg_power

    return cum_avg_pkg_power / n_samples


def sample_avg_dram_power(n_samples, sample_dur_secs):
    meter = pyRAPL.Measurement('energy')

    cum_dram_avg_power = 0.0

    for _ in range(n_samples):
        meter.begin()
        time.sleep(sample_dur_secs)
        meter.end()

        dram_energy = sum(meter.result.pkg) / 10**6
        dram_avg_power = dram_energy / meter.result.duration
        cum_dram_avg_power += dram_avg_power

    return cum_dram_avg_power / n_samples
