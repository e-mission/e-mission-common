"""
Functions for calculating the estimated footprint of a trip, both in terms of
energy usage (kwh) and carbon emissions (kg_co2).
"""

import emcommon.logger as Log
import emcommon.diary.base_modes as emcdb
import emcommon.metrics.footprint.egrid as emcmfe
import emcommon.metrics.footprint.transit as emcmft
import emcommon.metrics.footprint.util as emcmfu


def merge_metadatas(meta_a, meta_b):
    """
    Merge two metadata dictionaries, where child lists/arrays are concatenated and booleans are ORed.
    """
    # __pragma__('jsiter')
    for key in meta_b:
        # __pragma__('nojsiter')
        value = meta_b[key]
        if key not in meta_a:
            meta_a[key] = value
        elif hasattr(meta_a[key], 'concat'):
            meta_a[key] = meta_a[key].concat(value)
        elif isinstance(value, list):
            meta_a[key] = meta_a[key] + value
        elif isinstance(value, bool):
            meta_a[key] = meta_a[key] or value
        else:
            meta_a[key] = value


async def calc_footprint_for_trip(trip, mode_label_option):
    """
    Calculate the estimated footprint of a trip, which includes 'kwh' and 'kg_co2' fields.
    """
    Log.debug('Getting footprint for trip: ' + str(trip) +
              ', with mode option: ' + str(mode_label_option))
    metadata = {}
    distance = trip['distance']
    rich_mode = emcdb.get_rich_mode(mode_label_option)
    mode_footprint = dict(rich_mode['footprint'])
    if 'transit' in mode_footprint:
        (mode_footprint, transit_metadata) = await emcmft.get_transit_intensities_for_trip(trip, mode_footprint['transit'])
        merge_metadatas(metadata, transit_metadata)
    kwh_total = 0
    kg_co2_total = 0

    # __pragma__('jsiter')
    for fuel_type in mode_footprint:
        # __pragma__('nojsiter')
        fuel_type_footprint = mode_footprint[fuel_type]
        # distance in m converted to km; km * Wh/km results in Wh; convert to kWh
        kwh = (distance / 1000) * fuel_type_footprint['wh_per_km'] / 1000
        if fuel_type in emcmfu.FUELS_KG_CO2_PER_KWH:
            Log.debug('Using default carbon intensity for fuel type: ' + fuel_type)
            kg_co2 = kwh * emcmfu.FUELS_KG_CO2_PER_KWH[fuel_type]
        elif fuel_type == 'electric':
            Log.debug('Using eGRID carbon intensity for electric')
            (kg_per_kwh, egrid_metadata) = await emcmfe.get_egrid_intensity_for_trip(trip)
            merge_metadatas(metadata, egrid_metadata)
            kg_co2 = kwh * kg_per_kwh
        else:
            Log.warn('Unknown fuel type: ' + fuel_type)
            continue
        kwh_total += kwh
        kg_co2_total += kg_co2

    # Divide by number of passengers, if specified:
    # Some modes (air, transit modes) already account for this; the given footprints are per
    # passenger-km and 'passengers' is not defined.
    # Other modes (car, carpool) have a flexible number of passengers. The footprints are
    # per vehicle-km. Dividing by 'passengers' gives the footprint per passenger-km.
    passengers = mode_label_option['passengers'] if 'passengers' in mode_label_option else 1
    footprint = {
        'kwh': kwh_total / passengers,
        'kg_co2': kg_co2_total / passengers,
    }
    return (footprint, metadata)
