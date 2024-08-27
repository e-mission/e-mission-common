import json
import copy
import emcommon.metrics.footprint.util as util
from emcommon.metrics.footprint.louis_ntd_data_by_year import ntd_data as _ntd_data
# from emcommon.metrics.footprint.footprint_calculations import get_uace_by_zipcode

DIESEL_GGE = 1.136 # from energy.gov
KWH_PER_GALLON_GASOLINE = 33.7 # from the EPA, used as the basis for MPGe
KWH_PER_GALLON_DIESEL = KWH_PER_GALLON_GASOLINE * 1.14
# GGE constants found from https://epact.energy.gov/fuel-conversion-factors
KWH_PER_GALLON_BIODIESEL = KWH_PER_GALLON_GASOLINE * 1.05 
KWH_PER_GALLON_LPG = KWH_PER_GALLON_GASOLINE * .74
KWH_PER_GALLON_CNG = KWH_PER_GALLON_GASOLINE * .26
KWH_PER_KG_HYDROGEN = KWH_PER_GALLON_GASOLINE * 1.00


fuel_types = {
    "Diesel (mpg)": KWH_PER_GALLON_DIESEL,
    "Gasoline (mpg)": KWH_PER_GALLON_GASOLINE,
    "Liquefied Petroleum Gas (mpg)": KWH_PER_GALLON_LPG,
    "Compressed Natural Gas (mpg)": KWH_PER_GALLON_CNG,
    "Electric Propulsion (mi/kWh)": 1,
    "Electric Battery (mi/kWh)": 1,
    "Hydrogen (mpkg)": KWH_PER_KG_HYDROGEN,
}

def get_intensities_for_trip(trip, modes):
    year = util.year_of_trip(trip)
    uace_code = get_uace_by_zipcode(trip["start_confirmed_place"]["zipcode"], year)
    return get_intensities(year, uace_code, modes)

def get_intensities(year, uace, modes):
    ntd_data = copy.deepcopy(_ntd_data)
    year = str(year)
    code = uace

    aggregate_agencies = []
    total_passenger_trips = 0
    
    '''
    1. Sum up total passenger miles to calculate weight by agency later
    2. Calculate efficiency for each fuel
    3. Calculate weight of each fuel type
    4. Adjust miles using the weights to match mileage in service data
    5. Saved that data in aggregate_agencies
    '''
    for agency in ntd_data[year]:
        if agency["UACE Code"] == code and agency["Mode"] in modes:
            # Add up all the service data miles so we can calculate weight by agency later
            total_passenger_trips += agency["Unlinked Passenger Trips"]
            # Calculate the efficiency of each fuel
            for fuel_type in fuel_types: 
                wh_per_pkm = calculate_wh_per_pkm(agency, fuel_type)
                field_name = fuel_type.split(" (").pop(0) + " (wh/km)"
                agency[field_name] = wh_per_pkm
            # Calculate the weight of each fuel type and then add it in to the data
            fuel_weights = calculate_fuel_weights(agency)
            agency["fuel_weights"] = fuel_weights
            # Adjust miles using weights to match the mileage in the service data
            for fuel in fuel_weights:
                fuel_miles = fuel + " (miles)"
                agency[fuel_miles] = fuel_weights[fuel] * (agency["Train Miles"] or agency["Vehicle Miles"])
                # agency[fuel_miles] = fuel_weights[fuel] * (agency["Train Miles"] + agency["Vehicle Miles"])
            # Save all the agencies in one place
            aggregate_agencies.append(agency)
    
    fuel_averages = {
        "Diesel": [],
        "Gasoline": [],
        "Liquefied Petroleum Gas": [],
        "Compressed Natural Gas": [],
        "Electric Propulsion": [],
        "Electric Battery": [],
        "Hydrogen": []
    }

    '''
    6. Calculate weight by agency (% of passenger miles)
    7. Adjust the fuel weights using the weight by agency (fuel_weight * weight)
    8. Start aggregating data to use for the weighted average calculations
    '''
    for agency in aggregate_agencies:
        # Calculate weight by agency
        weight = agency["Unlinked Passenger Trips"] / total_passenger_trips
        agency["weight"] = weight
        # Adjust fuel weights
        for fuel_weight in agency["fuel_weights"]:
            agency["fuel_weights"][fuel_weight] *= weight
        # Add in data to calculate the weighted averages
        for fuel in fuel_averages:
            efficiency = agency[fuel + " (wh/km)"]
            weighted = agency["fuel_weights"][fuel]
            weighted_efficiency = efficiency * weighted
            fuel_averages[fuel].append((weighted_efficiency, weighted))

    '''
    9. Calculate weighted averages
    '''
    result = {}
    overall = 0
    for fuel in fuel_averages:
        combined_weighted_efficiency = 0
        combined_weighted = 0
        weighted_average = 0
        for (weighted_efficiency, weighted) in fuel_averages[fuel]:
            combined_weighted_efficiency += weighted_efficiency
            combined_weighted += weighted
        if combined_weighted != 0:
            weighted_average = combined_weighted_efficiency / combined_weighted
        result[fuel] = {
            "wh_per_pkm": weighted_average,
            "weight": combined_weighted
        }
        overall += (weighted_average * combined_weighted)
    result['overall'] = {
        'wh_per_km': overall,
        'weight': 1.0
    }
    return result
    
def calculate_wh_per_pkm(agency, fuel_type):
    fuel = agency[fuel_type]
    # Convert to km
    km_per_gallon = fuel * 1.60934
    # Convert to wh
    wh_per_km = 0
    if km_per_gallon != 0:
        wh_per_km = (fuel_types[fuel_type] * 1000) / km_per_gallon
    # load_factor = agency["Passenger Miles Traveled"] / (agency["Vehicle Miles"] + agency["Train Miles"]) 
    load_factor = agency["Passenger Miles Traveled"] / (agency["Train Miles"] or agency["Vehicle Miles"]) 
    wh_per_pkm = wh_per_km / load_factor
    return wh_per_pkm

def calculate_fuel_weights(agency):
    fuels = ["Diesel (miles)","Gasoline (miles)","Liquefied Petroleum Gas (miles)","Compressed Natural Gas (miles)","Hydrogen (miles)","Electric Propulsion (miles)","Electric Battery (miles)"]
    fuel_weights = {}
    for fuel in fuels:
        pct = 0
        if agency["All Fuels (miles)"] != 0:
            pct = agency[fuel] / agency["All Fuels (miles)"]
        field_name = fuel.split(" (").pop(0)
        fuel_weights[field_name] = pct
    return fuel_weights
    


trip = {
    "year": "2022",
    "code": "16264"
}
modes = ["LR", "HR", "YR", "CR"]
get_intensities("2022", "16264", modes)
