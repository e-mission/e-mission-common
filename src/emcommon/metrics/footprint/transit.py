"""
Functions that utilize NTD data to estimate fuel efficiency of different public transit
modes in a given year and area code.
"""

from __future__ import annotations  # __: skip
import emcommon.logger as Log
import emcommon.metrics.footprint.util as util

fuel_types = ['Gasoline', 'Diesel', 'LPG', 'CNG', 'Hydrogen', 'Electric', 'Other']


def weighted_mean(values, weights):
    w_sum = sum(weights)
    return sum([v * w / w_sum for v, w in zip(values, weights)])


async def get_transit_intensities(year: int, coords: list[float, float] = None,
                                  uace: str | None = None, modes: list[str] | None = None,
                                  metadata: dict = {}):
    # Log.debug(f"Getting mode footprint in year {year}, coords {coords}, "
    #           f"UACE {uace}, and modes {modes}")
    if uace is None:
        metadata.update({'requested_coords': coords})
        uace = await util.get_uace_by_coords(coords, year)
    return await get_transit_intensities_for_uace(year, uace, modes, metadata)


async def get_transit_intensities_for_uace(year: int, uace: str | None = None, modes: list[str] | None = None, metadata: dict = {}):
    """
    Returns estimated energy intensities by fuel type across the given modes in the urban area of the given trip.
    :param trip: The trip to get the data for, e.g. {"year": "2022", "distance": 1000, "start_loc": {"coordinates": [-84.52, 39.13]}}
    :param modes: The NTD modes to get the data for, e.g. ["MB","CB"] (https://www.transit.dot.gov/ntd/national-transit-database-ntd-glossary)
    :returns: A dictionary of energy intensities by fuel type, with weights, e.g. {"gasoline": { "wh_per_km": 1000, "weight": 0.5 }, "diesel": { "wh_per_km": 2000, "weight": 0.5 }, "overall": { "wh_per_km": 1500, "weight": 1.0 } }
    """
    # Log.debug(f"Getting mode footprint for transit modes {modes} in year {year} and UACE {uace}")
    intensities_data = await util.get_intensities_data(year, 'ntd')
    actual_year = intensities_data['metadata']['year']
    metadata.update({
        "data_sources": [f"ntd{actual_year}"],
        "data_source_urls": intensities_data['metadata']['data_source_urls'],
        "is_provisional": actual_year != year,
        "requested_year": year,
        "ntd_uace_code": uace,
        "ntd_modes": modes,
        "ntd_ids": [],
    })

    total_upt = 0
    agency_mode_fueltypes = []
    for entry in intensities_data['records']:
        # skip entries that don't match the requested modes or UACE
        if (modes and entry["Mode"] not in modes) or (uace and entry["UACE Code"] != uace):
            continue
        upt = entry['Unlinked Passenger Trips']
        total_upt += upt
        for fuel_type in fuel_types:
            fuel_pct = entry[f"{fuel_type} (%)"] if f"{fuel_type} (%)" in entry else 0
            wh_per_pkm = entry[f"{fuel_type} (Wh/pkm)"] if f"{fuel_type} (Wh/pkm)" in entry else 0
            if fuel_pct and wh_per_pkm:
                agency_mode_fueltypes.append({
                    "fuel_type": fuel_type,
                    "upt": fuel_pct / 100 * upt,
                    "wh_per_km": wh_per_pkm
                })
                if entry['NTD ID'] not in metadata["ntd_ids"]:
                    metadata["ntd_ids"].append(entry['NTD ID'])

    # TODO Should there be a threshold for the minimum amount of data required?
    # i.e. if there is only one tiny agency that matches the criteria, should we trust it?
    # if total_upt < 10000:

    if not agency_mode_fueltypes:
        if uace:
            Log.info(f"Insufficient data for year {year} and UACE {uace} and modes {modes}. "
                     "Retrying with UACE=None")
            return await get_transit_intensities_for_uace(year, None, modes)
        if modes:
            Log.info(f"Insufficient data for year {year} and UACE {uace} and modes {modes}. "
                     "Retrying with modes = None")
            return await get_transit_intensities_for_uace(year, uace, None)
        Log.error("No data available for any UACE or modes")
        return (None, metadata)

    for entry in agency_mode_fueltypes:
        entry['weight'] = entry['upt'] / total_upt
    # Log.debug(f"agency_mode_fueltypes = {agency_mode_fueltypes}"[:500])

    intensities = {}
    for fuel_type in fuel_types:
        fuel_type_entries = [entry for entry in agency_mode_fueltypes
                             if entry['fuel_type'] == fuel_type]
        if len(fuel_type_entries) == 0:
            continue
        wh_per_km_values = [entry['wh_per_km'] for entry in fuel_type_entries]
        weights = [entry['weight'] for entry in fuel_type_entries]
        # Log.debug(
        #     f"fuel_type = {fuel_type}; wh_per_km_values = {wh_per_km_values}; weights = {weights}"[:500])
        fuel_type = fuel_type.lower()
        intensities[fuel_type] = {
            "wh_per_km": weighted_mean(wh_per_km_values, weights),
            "weight": sum(weights)
        }

    # take the overall weighted average between fuel types
    wh_per_km_values = [entry['wh_per_km'] for entry in agency_mode_fueltypes]
    weights = [entry['weight'] for entry in agency_mode_fueltypes]
    intensities['overall'] = {
        "wh_per_km": weighted_mean(wh_per_km_values, weights),
        "weight": sum(weights)
    }

    # Log.info(f"intensities = {intensities}")
    # Log.info(f"metadata = {metadata}"[:500])
    return (intensities, metadata)
