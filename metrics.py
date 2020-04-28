"""
[1] https://www.eea.europa.eu/data-and-maps/daviz/sds/co2-emission-intensity-from-electricity-generation-2/@@view
[2] Giving What We Can: Cool Earth, Retrieved 28-04-2020, https://www.givingwhatwecan.org/report/cool-earth/#3-overall-evaluation 
[3] https://calculator.carbonfootprint.com/calculator.aspx?tab=3
NOTE: [3] is not a legitimate source of where the number came from. We should investigate further
"""

"""
United Kingdom national average for kg of CO2 emissions per kWh [1]
"""
KG_CO2_PER_KWH = 0.281

"""
Cost (in USD) to offset a kg of CO2 if donated to Cool Earth [2]
"""
USD_PER_KG_CO2 = 1.34 / 1000

"""
Estimate of kg of CO2 per person per one-way flight from London to New York [3]
"""
KG_CO2_PER_FLIGHT = 1.67


def carbon_offset_cost(kWh):
    """
    Donation to Cool Earth (in USD) needed to offset carbon emssions.
    """
    return KG_CO2_PER_KWH * USD_PER_KG_CO2 * kWh


def number_of_flights(kWh):
    """
    Equivalent number of one-way flights from London to New York.
    """
    return KG_CO2_PER_KWH * kWh / KG_CO2_PER_FLIGHT
