from __future__ import annotations  # __: skip
import emcommon.logger as Log
from emcommon.util import read_json_resource, fetch_url

MI_PER_KM = 0.621371

# 114,000 BTU / gal -> 33.41 kWh / gal
# consistent with DOE ranges for lower heating value (112,114 – 116,090)
# this is used for energy intensities
KWH_PER_GGE = 33.41

# MPGe is based on EPA's conversion factor, slightly higher than DOE / GREET
# this is ONLY used to convert MPGe to Wh/km
MPGE_KWH_PER_GAL = 33.7  # 33.7 kWh per gallon of gasoline equivalent

# GGE constants found from https://epact.energy.gov/fuel-conversion-factors
KWH_PER_GAL_GASOLINE = KWH_PER_GGE * 1.00
KWH_PER_GAL_DIESEL = KWH_PER_GGE * 1.14
KWH_PER_GAL_BIODIESEL = KWH_PER_GGE * 1.05
KWH_PER_GAL_LPG = KWH_PER_GGE * .74
KWH_PER_GAL_CNG = KWH_PER_GGE * .26  # based on 3600 psi, industry standard
KWH_PER_KG_HYDROGEN = KWH_PER_GGE * 1.00
# TODO can we handle the default case better? https://github.com/JGreenlee/e-mission-common/pull/3#discussion_r1739188643
KWH_PER_GAL_OTHER = KWH_PER_GGE * 1.00

# from CHEER paper 2024
FUELS_KG_CO2_PER_MWH = {
    'gasoline': 324.183,
    'diesel': 325.073,
    'jet_fuel': 304.354,
    'lpg': 279.192,
    'cng': 271.024,
    'hydrogen': 332.852,
}


def mpge_to_wh_per_km(mpge: float) -> float:
    """
    Convert miles per gallon of gasoline equivalent (MPGe) to watt-hours per kilometer.
    e.g. mpge_to_wh_per_km(100) -> 209.40202700000003
    """
    return MI_PER_KM / mpge * MPGE_KWH_PER_GAL * 1000


def year_of_trip(trip) -> int:
    return int(trip['start_fmt_time'].split('-')[0])


# raytracing algorithm
def is_point_inside_polygon(pt, vs):
    x, y = pt
    inside = False
    j = len(vs) - 1
    for i in range(len(vs)):
        xi, yi = vs[i]
        xj, yj = vs[j]
        intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
        if intersect:
            inside = not inside
        j = i
    return inside


def get_feature_containing_point(pt, geojson):
    """
    Find the first feature in the given GeoJSON that contains the given point.
    """
    for feature in geojson['features']:
        if feature['geometry']['type'] == 'Polygon':
            polys = [feature['geometry']['coordinates']]
        elif feature['geometry']['type'] == 'MultiPolygon':
            polys = feature['geometry']['coordinates']
        for poly in polys:
            if is_point_inside_polygon(pt, poly[0]):
                return feature
    return None


latest_egrid_year = None
latest_ntd_year = None


async def get_egrid_region(coords: list[float, float], year: int) -> str | None:
    """
    Get the eGRID region at the given coordinates in the year.
    """
    global latest_egrid_year
    if year < 2018:
        Log.warn(f"eGRID data not available for {year}. Using 2018.")
        return await get_egrid_region(coords, 2018)
    if latest_egrid_year is not None and year > latest_egrid_year:
        return await get_egrid_region(coords, latest_egrid_year)
    try:
        geojson = await read_json_resource(f"egrid{year}_subregions_5pct.json")
    except:
        if year > 2018:
            Log.warn(f"eGRID data not available for {year}. Trying {year-1}.")
            latest_egrid_year = year-1
            return await get_egrid_region(coords, year-1)
        Log.error(f"eGRID lookup failed for {year}.")
        return None
    region_feature = get_feature_containing_point(coords, geojson)
    if region_feature is not None:
        return region_feature['properties']['name']
    Log.warn(f"An eGRID region was not found for coords {coords} in year {year}.")
    return None


async def get_uace_by_coords(coords: list[float, float], year: int) -> str | None:
    """
    Get the UACE code for the given coordinates in the given year.
    """

    census_year = year - (year % 10)  # round down to the nearest decade
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?" + \
        f"x={coords[0]}&y={coords[1]}" + \
        f"&benchmark=Public_AR_Current&vintage=Census{census_year}_Current&layers=87&format=json"

    try:
        data = await fetch_url(url)
    except Exception as e:
        Log.error(f"Failed to geocode {coords} in year {year}: {e}")
        return None
    except:
        Log.error(f"Failed to geocode {coords} in year {year}")
        return None

    # __pragma__('jsiter')
    for g in data['result']['geographies']:
        # __pragma__('nojsiter')
        for entry in data['result']['geographies'][g]:
            if 'UA' in entry:
                return entry['UA']
    Log.warn(f"Urban Area not in geocoding response for coords {coords} in year {year}: {url}")
    return None


async def get_intensities_data(year: int, dataset: str) -> dict:
    """
    Get the 'intensities' data for the given year from the specified dataset.
    """
    global latest_egrid_year, latest_ntd_year
    if year < 2018:
        Log.warn(f"{dataset} data not available for {year}. Using 2018.")
        return await get_intensities_data(2018, dataset)
    if dataset == 'egrid' and latest_egrid_year is not None and year > latest_egrid_year:
        return await get_intensities_data(latest_egrid_year, dataset)
    if dataset == 'ntd' and latest_ntd_year is not None and year > latest_ntd_year:
        return await get_intensities_data(latest_ntd_year, dataset)
    try:
        return await read_json_resource(f"{dataset}{year}_intensities.json")
    except:
        if year > 2018:
            Log.warn(f"{dataset} data not available for {year}. Trying {year-1}.")
            if dataset == 'egrid':
                latest_egrid_year = year-1
            elif dataset == 'ntd':
                latest_ntd_year = year-1
            return await get_intensities_data(year-1, dataset)
        Log.error(f"eGRID lookup failed for {year}.")
        return None
