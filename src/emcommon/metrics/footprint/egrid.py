from __future__ import annotations  # __: skip
import emcommon.logger as Log
import emcommon.metrics.footprint.util as emcmfu


async def get_egrid_intensity(year: int, coords: list[float, float] | None = None,
                              region: str | None = None, metadata: dict = {}):
    # Log.debug(f"Getting eGRID carbon intensity for year {year}, coords {coords}, "
    #           f"and region {region}")
    if region is None:
        metadata.update({'requested_coords': coords})
        region = await emcmfu.get_egrid_region(coords, year)
    return await get_egrid_intensity_for_region(year, region, metadata)


async def get_egrid_intensity_for_region(year: int, region: str | None, metadata: dict = {}):
    """
    Returns the estimated carbon intensity of the electricity grid at the given region for the given year (units in kg CO2e per MWh).
    :param year: The year as int, e.g. 2022
    :param region: The region as str, e.g. "NWPP"
    """
    # Log.debug(f"Getting eGRID carbon intensity for year {year} and region {region}")
    intensities_data = await emcmfu.get_intensities_data(year, 'egrid')
    actual_year = intensities_data['metadata']['year']
    metadata.update({
        "data_sources": [f"egrid{actual_year}"],
        "data_source_urls": intensities_data['metadata']['data_source_urls'],
        "is_provisional": actual_year != year,
        "requested_year": year,
        "egrid_region": region,
    })
    if region is not None and region in intensities_data['regions_kg_per_mwh']:
        kg_per_kwh = intensities_data['regions_kg_per_mwh'][region]
    else:
        Log.warn(f"eGRID region not found for region {region} in year {year}. "
                 "Using national average.")
        kg_per_kwh = intensities_data['national_kg_per_mwh']
    return (kg_per_kwh, metadata)
