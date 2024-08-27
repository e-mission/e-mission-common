from __future__ import annotations  # __: skip
import emcommon.logger as Log
from emcommon.util import read_json_resource, fetch_url

# https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references

KWH_PER_GAL_GASOLINE = 33.7  # from the EPA, used as the basis for MPGe
DIESEL_GGE = 0.88  # .88 gal diesel ≈ 1 gal gasoline
KWH_PER_GAL_DIESEL = KWH_PER_GAL_GASOLINE * 1.14
# GGE constants found from https://epact.energy.gov/fuel-conversion-factors
KWH_PER_GAL_BIODIESEL = KWH_PER_GAL_GASOLINE * 1.05
KWH_PER_GAL_LPG = KWH_PER_GAL_GASOLINE * .74
KWH_PER_GAL_CNG = KWH_PER_GAL_GASOLINE * .26
KWH_PER_KG_HYDROGEN = KWH_PER_GAL_GASOLINE * 1.00
KWH_PER_GAL_OTHER = KWH_PER_GAL_GASOLINE * 1.00  # TODO find a better default value

# GREET2023 Co2(x/ C in VOC & CO) results
# (converted g/mmBTU values to kg/Gal fuel using constants and LHVs in Fuel_Specs
# from "gasoline vehicle" (ensured alignment with HEV and PHEV in CS mode)
KG_CO2_PER_GALLON_GASOLINE = 10.15
# from "CIDI Vehicle: Conventional and LS Diesel"
KG_CO2_PER_GALLON_DIESEL = 11.79

FUELS_KG_CO2_PER_KWH = {
    # 8.89 kg CO2 / gal (EPA)
    'gasoline': KG_CO2_PER_GALLON_GASOLINE / KWH_PER_GAL_GASOLINE,
    # 10.18 kg CO2 / gal (EPA)
    'diesel': KG_CO2_PER_GALLON_DIESEL / (KWH_PER_GAL_GASOLINE / DIESEL_GGE),
    # 0.25 kg CO2 / kWh (https://www.eia.gov/environment/emissions/co2_vol_mass.php)
    'jet_fuel': 0.25,

    'cng': 0.25,  # TODO !!
    'lpg': 0.25,  # TODO !!
}

MI_PER_KM = 0.621371


def mpge_to_wh_per_km(mpge: float) -> float:
    """
    Convert miles per gallon of gasoline equivalent (MPGe) to watt-hours per kilometer.
    e.g. mpge_to_wh_per_km(100) -> 209.40202700000003
    """
    return MI_PER_KM / mpge * KWH_PER_GAL_GASOLINE * 1000


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


async def get_egrid_region(coords: list[float, float], year: int) -> str | None:
    """
    Get the eGRID region at the given coordinates in the year.
    """
    if year < 2018:
        Log.warn(f"eGRID data not available for {year}. Using 2018.")
        return await get_egrid_region(coords, 2018)
    try:
        geojson = await read_json_resource(f"egrid{year}_subregions_5pct.json")
    except:
        if year > 2018:
            Log.warn(f"eGRID data not available for {year}. Trying {year-1}.")
            return await get_egrid_region(coords, year-1)
        Log.error(f"eGRID lookup failed for {year}.")
        return None
    region_feature = get_feature_containing_point(coords, geojson)
    if region_feature is not None:
        return region_feature['properties']['name']
    # __pragma__('noskip')
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
    Log.error(
        f"Geocoding response did not contain UA for coords {coords} in year {year}: {data}")
    return None


async def get_intensities_data(year: int, dataset: str) -> dict:
    """
    Get the 'intensities' data for the given year from the specified dataset.
    """
    if year < 2018:
        Log.warn(f"{dataset} data not available for {year}. Using 2018.")
        return await get_intensities_data(2018, dataset)
    try:
        return await read_json_resource(f"{dataset}{year}_intensities.json")
    except:
        if year > 2018:
            Log.warn(f"{dataset} data not available for {year}. Trying {year-1}.")
            return await get_intensities_data(year-1, dataset)
        Log.error(f"eGRID lookup failed for {year}.")
        return None
