"""
Functions for calculating the estimated footprint of a trip, both in terms of
energy usage (kwh) and carbon emissions (kg_co2).
"""

#GREET2023 Co2(x/ C in VOC & CO) results 
#(converted g/mmBTU values to kg/Gal fuel using constants and LHVs in Fuel_Specs
#from "gasoline vehicle" (ensured alignment with HEV and PHEV in CS mode)
KG_CO2_PER_GALLON_GASOLINE = 10.15
#from "CIDI Vehicle: Conventional and LS Diesel"
KG_CO2_PER_GALLON_DIESEL = 11.79

DIESEL_GGE = 1.136 # from energy.gov
KWH_PER_GALLON_GASOLINE = 33.7 # from the EPA, used as the basis for MPGe
KWH_PER_GALLON_DIESEL = KWH_PER_GALLON_GASOLINE * 1.14

KG_CO2_PER_KWH_GASOLINE = KG_CO2_PER_GALLON_GASOLINE / KWH_PER_GALLON_GASOLINE
KG_CO2_PER_KWH_DIESEL = KG_CO2_PER_GALLON_DIESEL / KWH_PER_GALLON_DIESEL

def grid_emission_rate_for_trip(trip):
  # TODO
  pass

def calc_footprint_for_trip(trip, mode_footprint):
  """
  Calculate the estimated footprint of a trip, which includes 'kwh' and 'kg_co2' fields.
  """
  distance = trip['distance']
  kwh_total = 0
  kg_co2_total = 0
  for fuel_type, fuel_type_footprint in mode_footprint.items():
    # distance in m converted to km; km * Wh/km results in Wh; convert to kWh
    kwh = (distance / 1000) * fuel_type_footprint['wh_per_km'] / 1000
    if fuel_type == 'electric':
      kg_per_kwh = grid_emission_rate_for_trip(trip)
      kg_co2 = kwh * kg_per_kwh
    if fuel_type == 'gasoline':
      kg_co2 = kwh * KG_CO2_PER_KWH_GASOLINE
    if fuel_type == 'diesel':
      kg_co2 = kwh * KG_CO2_PER_KWH_DIESEL
    kwh_energy += kwh
    kg_co2_total += kg_co2

  return {
    'kwh': kwh_total,
    'kg_co2': kg_co2_total
  }
