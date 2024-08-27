from __future__ import annotations  # __: skip
import emcommon.logger as Log


def get_ble_sensed_vehicle_for_section(ble_entries, start_ts, end_ts, app_config):
    """
    Returns the vehicle that was sensed via BLE beacon during the section.
    """
    Log.debug('getting BLE sensed vehicle for section from %d to %d' % (start_ts, end_ts))
    if 'vehicle_identities' not in app_config:
        return None
    ble_ranging_entries_during_section = get_ble_range_updates_for_section(
        ble_entries, start_ts, end_ts
    )
    Log.debug('After filtering, %d BLE ranging entries during the section' %
              len(ble_ranging_entries_during_section))
    if len(ble_ranging_entries_during_section) == 0:
        return None

    # The beacon that was seen the most times during the section is the one we will use
    ble_beacon_counts = {}
    for entry in ble_ranging_entries_during_section:
        # major:minor formatted as 4-character hexadecimal strings, e.g. 'f00d:cafe'
        major_minor = "{:02x}".format(
            entry['data']['major']) + ":" + "{:02x}".format(entry['data']['minor'])
        if major_minor not in ble_beacon_counts:
            ble_beacon_counts[major_minor] = 0
        ble_beacon_counts[major_minor] += 1
    Log.debug('after counting, ble_beacon_counts = %s' % ble_beacon_counts)
    ble_beacon_major_minor = max(ble_beacon_counts, key=ble_beacon_counts.get)
    return get_vehicle_with_ble_beacon(ble_beacon_major_minor, app_config)


def decimal_to_hex_string(n: int, min_length: int = 0) -> str:
    """
    Convert a decimal number to a hexadecimal string, with optional padding to reach the desired length.
    - e.g. decimal_to_hex_string(245) => 'f5'
    - e.g. decimal_to_hex_string(245, 4) => '00f5'
    """
    # In JS we can use toString(16) to convert a number to a hexadecimal string
    '''?
    hex = Number(n).toString(16);
    ?'''
    # In Python we can use an f-string with the :x format specifier
    hex = f'{n:x}'  # __: skip

    # apply padding if necessary to reach the desired length
    while len(hex) < min_length:
        hex = '0' + hex
    return hex


def get_ble_range_updates_for_section(ble_entries, start_ts, end_ts):
    """
    Returns the BLE ranging entries that occurred during the section.
    """
    return [
        entry for entry in ble_entries
        if entry['data']['ts'] >= start_ts
        and entry['data']['ts'] <= end_ts
        and (
            entry['data']['eventType'] == 'RANGE_UPDATE'
            # the server uses an enum (BLEEventTypes.RANGE_UPDATE), so once processed this becomes 2
            or entry['data']['eventType'] == 2
        )
    ]


def get_vehicle_with_ble_beacon(major_minor, app_config):
    """
    Returns the vehicle that is assigned to the BLE beacon with the given major:minor string.
    """
    for vehicle in app_config['vehicle_identities']:
        if major_minor in vehicle['bluetooth_major_minor']:
            Log.debug('found vehicle %s with BLE beacon %s' % (vehicle['text'], major_minor))
            return vehicle
    Log.debug('no vehicle found for BLE beacon %s' % major_minor)
    return None


def primary_ble_sensed_mode_for_trip(trip) -> str:
    """
    Returns the primary BLE sensed mode for the trip (the mode with the greatest distance).
    """
    if 'ble_sensed_summary' not in trip or 'distance' not in trip['ble_sensed_summary']:
        return None
    dists = trip['ble_sensed_summary']['distance']
    dists = dists if type(dists) == dict else dict(dists)
    # return the key of the mode with the greatest distance
    high = (None, 0)
    for k, v in dists.items():
        high = (k, v) if v > high[1] else high
    return high[0]
