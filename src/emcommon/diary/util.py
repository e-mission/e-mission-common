from __future__ import annotations  # __: skip

import emcommon.logger as Log
import emcommon.bluetooth.ble_matching as emcble


def label_for_trip(composite_trip: dict, label_key: str, labels_map=None) -> str | None:
    """
    :param composite_trip: composite trip
    :param label_key: which type of label to get ('mode', 'purpose', or 'replaced_mode')
    :return: the label for the trip, derived from the trip's user_input if available, or the labels_map if available, or 'unlabeled' otherwise
    """
    label_key = label_key.upper()
    label_key_confirm = label_key.lower() + '_confirm'
    if 'user_input' in composite_trip and label_key_confirm in composite_trip['user_input']:
        return composite_trip['user_input'][label_key_confirm]
    if labels_map and composite_trip['_id']['$oid'] in labels_map \
            and label_key in labels_map[composite_trip['_id']['$oid']]:
        return labels_map[composite_trip['_id']['$oid']][label_key]['data']['label']
    return None


def survey_answered_for_trip(composite_trip: dict, labels_map=None) -> str | None:
    """
    :param composite_trip: composite trip
    :return: the name of the survey that was answered for the trip, or None if no survey was answered
    """
    if 'user_input' in composite_trip and 'trip_user_input' in composite_trip['user_input']:
        return composite_trip['user_input']['trip_user_input']['data']['name']
    if labels_map and composite_trip['_id']['$oid'] in labels_map:
        survey = dict(labels_map[composite_trip['_id']['$oid']]).values()[0]
        return survey['data']['name']
    return None


def primary_inferred_mode_for_trip(trip: dict, labels_map=None) -> str:
    return None  # TODO


def primary_sensed_mode_for_trip(trip: dict) -> str:
    """
    Get the mode with the greatest distance in the cleaned_section_summary
    """
    if 'cleaned_section_summary' not in trip:
        return None
    dists = dict(trip['cleaned_section_summary']['distance'])
    return max(dists, key=dists.get)


def primary_mode_for_trip(trip: dict, labels_map=None) -> str:
    """
    :param trip: confirmed trip
    :return: The best mode for the trip, as determined by the following order:
        - Labeled mode (trip.user_input.mode_confirm)
        - BLE sensed mode (trip.ble_sensed_summary with greatest distance)
        - Inferred mode (trip.inferred_labels with greatest confidence)
        - Sensed mode (trip.cleaned_section_summary with greatest distance)
        - None
    """
    return label_for_trip(trip, 'mode', labels_map) \
        or emcble.primary_ble_sensed_mode_for_trip(trip) \
        or primary_inferred_mode_for_trip(trip, labels_map) \
        or primary_sensed_mode_for_trip(trip) \
        or None
