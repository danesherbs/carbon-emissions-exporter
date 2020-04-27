from prometheus_client import start_http_server, Gauge, Counter
import pyRAPL
import gpumeter
import time

from meters import *

# Constants
#     KG_CO2_PER_KWH: An average kg of CO2 per kWh in United Kingdom: 0.281 kg CO2 per kWh [1]
#     KG_CO2_PER_USD: A pessimistic estimation of the cost to reduce 1 tonne of CO2: $1.34
#     (could be as low as $0.38 if counted indirectly shielded forests) [2][3]
#     KG_CO2_PER_FLIGHT: An average kg of CO2 per person during a single trip economy flight from London to New York [4]
#     Source:
#     [1] https://www.eea.europa.eu/data-and-maps/daviz/sds/co2-emission-intensity-from-electricity-generation-2/@@view
#     [2] "ClimateCare." 2006. 12 Jan. 2016 <http://climatecare.org/>
#     [3] "Carbon Footprint Ltd - Carbon Management Services …" 2003. 12 Jan. 2016 <http://www.carbonfootprint.com/>
#     [4] https://calculator.carbonfootprint.com/calculator.aspx?tab=3
#     NOTE: [4] is not a legitimate source of where the number came from. We should investigate further
KG_CO2_PER_KWH = 0.281
KG_CO2_PER_USD = 1.34
KG_CO2_PER_FLIGHT = 1.67

def carbon_offset_cost(kWh):
    """
    Cost to offset kWh of energy consumption in USD
    """
    return KG_CO2_PER_KWH * kWh / KG_CO2_PER_USD


def number_of_flights(kWh):
    """
    Number of flights from London to New York a given energy consumption (kWh) is equivalent of generating
    """
    return KG_CO2_PER_KWH * kWh / KG_CO2_PER_FLIGHT
