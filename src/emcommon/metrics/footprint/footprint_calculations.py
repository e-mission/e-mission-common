"""
Functions for calculating the estimated footprint of a trip, both in terms of
energy usage (kwh) and carbon emissions (kg_co2).
"""

import emcommon.logger as Log
import emcommon.diary.base_modes as emcdb
import emcommon.diary.util as emcdu
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
            meta_a[key] = meta_a[key].concat([v for v in value if v not in meta_a[key]])
        elif isinstance(value, list):
            meta_a[key] = meta_a[key] + [v for v in value if v not in meta_a[key]]
        elif isinstance(value, bool):
            meta_a[key] = meta_a[key] or value
        else:
            meta_a[key] = value


async def calc_footprint_for_trip(trip, label_options, mode_value=None, labels_map=None):
    """
    Calculate the estimated footprint of a trip, which includes 'kwh' and 'kg_co2' fields.
    """
    trip = dict(trip)
    # Log.debug(f"Getting footprint for trip: {str(trip)}")
    mode_value = mode_value or emcdu.label_for_trip(trip, 'mode', labels_map)
    rich_mode = mode_value and emcdb.get_rich_mode_for_value(mode_value, label_options)
    is_uncertain = False
    if rich_mode is None or 'footprint' not in rich_mode:
        # Log.warn(f"Mode {str(rich_mode)} does not have a footprint."
        #          "Using worst rich mode to determine uncertainty.")
        is_uncertain = True
        rich_mode = find_worst_rich_mode(label_options)

    (footprint, metadata) = await calc_footprint(
        rich_mode['footprint'],
        trip['distance'],
        emcmfu.year_of_trip(trip),
        trip['start_loc']['coordinates'],
        uace=trip.get('uace_region'),
        egrid_region=trip.get('egrid_region'),
        passengers=rich_mode.get('passengers', 1),
        metadata={'trip_id': trip['_id']}
    )
    # If is_uncertain, the kwh and kg_co2 values represent the upper bound (worst-case scenario)
    # Mark them as them uncertain, then set the main values to 0 to represent the lower bound.
    if is_uncertain:
        footprint['kwh_uncertain'] = footprint['kwh']
        footprint['kg_co2_uncertain'] = footprint['kg_co2']
        footprint['kwh'] = 0
        footprint['kg_co2'] = 0
    return (footprint, metadata)


async def calc_footprint(mode_footprint, distance, year, coords, uace=None,
                         egrid_region=None, passengers=1, metadata={}):
    mode_footprint = dict(mode_footprint)
    if 'transit' in mode_footprint:
        (mode_footprint, transit_metadata) = await emcmft.get_transit_intensities(
            year, coords, uace, mode_footprint['transit']
        )
        merge_metadatas(metadata, transit_metadata)
    kwh_total = 0
    kg_co2_total = 0

    for fuel_type in mode_footprint.keys():
        fuel_type_footprint = mode_footprint[fuel_type]
        kwh = 0
        if 'wh_per_km' in fuel_type_footprint:
            # distance in m converted to km; km * Wh/km results in Wh; convert to kWh
            kwh += (distance / 1000) * fuel_type_footprint['wh_per_km'] / 1000
        if 'wh_per_trip' in fuel_type_footprint:
            kwh += fuel_type_footprint['wh_per_trip'] / 1000

        if fuel_type in emcmfu.FUELS_KG_CO2_PER_MWH:
            # Log.debug('Using default carbon intensity for fuel type: ' + fuel_type)
            kg_co2 = (kwh / 1000) * emcmfu.FUELS_KG_CO2_PER_MWH[fuel_type]
        elif fuel_type == 'electric':
            # Log.debug('Using eGRID carbon intensity for electric')
            (kg_per_mwh, egrid_metadata) = await emcmfe.get_egrid_intensity(
                year, coords, egrid_region
            )
            merge_metadatas(metadata, egrid_metadata)
            kg_co2 = kwh * kg_per_mwh / 1000
        elif fuel_type != 'overall':
            Log.warn('Unknown fuel type: ' + fuel_type)
            continue

        weight = fuel_type_footprint['weight'] if 'weight' in fuel_type_footprint else 1
        kwh_total += kwh * weight
        kg_co2_total += kg_co2 * weight

    # Divide by number of passengers, if specified:
    # Some modes (air, transit modes) already account for this; the given footprints are per
    # passenger-km and 'passengers' is not defined.
    # Other modes (car, carpool) have a flexible number of passengers. The footprints are
    # per vehicle-km. Dividing by 'passengers' gives the footprint per passenger-km.
    footprint = {
        'kwh': kwh_total / passengers,
        'kg_co2': kg_co2_total / passengers,
    }
    return (footprint, metadata)


_worst_rich_mode = None
_worst_wh_per_km = 0


def find_worst_rich_mode(label_options):
    """
    Given these label options, find the mode option with the highest wh_per_km (any fuel type)
    Usually this will be taxi/ridehail but could be something else defined by deployers
    """
    global _worst_rich_mode, _worst_wh_per_km
    if _worst_rich_mode is not None:
        return _worst_rich_mode
    for opt in label_options['MODE']:
        rm = emcdb.get_rich_mode(opt)
        if 'footprint' not in rm or 'transit' in rm['footprint']:
            continue
        mode_footprint = dict(rm['footprint'])
        for fuel_type in mode_footprint.keys():
            if 'wh_per_km' in rm['footprint'][fuel_type]:
                wh_per_km = rm['footprint'][fuel_type]['wh_per_km']
                if wh_per_km > _worst_wh_per_km:
                    _worst_rich_mode = rm
                    _worst_wh_per_km = wh_per_km
    Log.debug(f"Worst rich mode is {str(_worst_rich_mode['value'])} with "
              f"{str(_worst_wh_per_km)} wh_per_km")
    return _worst_rich_mode
