from __future__ import annotations  # __: skip
# from util import memoize
import emcommon.logger as Log
import emcommon.util as util
import emcommon.bluetooth.ble_matching as emcble
import emcommon.survey.conditional_surveys as emcsc

app_config = None
labels_map = None

# @memoize


def label_for_trip(composite_trip: dict, label_key: str) -> str:
    """
    :param composite_trip: composite trip
    :param label_key: which type of label to get ('mode', 'purpose', or 'replaced_mode')
    :return: the label for the trip, derived from the trip's user_input if available, or the labels_map if available, or 'unlabeled' otherwise
    """
    global labels_map
    label_key = label_key.upper()
    label_key_confirm = label_key.lower() + '_confirm'
    if 'user_input' in composite_trip and label_key_confirm in composite_trip['user_input']:
        return composite_trip['user_input'][label_key_confirm]
    if labels_map and composite_trip['_id']['$oid'] in labels_map \
            and label_key in labels_map[composite_trip['_id']['$oid']]:
        return labels_map[composite_trip['_id']['$oid']][label_key]['data']['label']
    return None


def survey_answered_for_trip(composite_trip: dict) -> str | None:
    """
    :param composite_trip: composite trip
    :return: the name of the survey that was answered for the trip, or None if no survey was answered
    """
    global labels_map
    if 'user_input' in composite_trip and 'trip_user_input' in composite_trip['user_input']:
        return composite_trip['user_input']['trip_user_input']['data']['name']
    if labels_map and composite_trip['_id']['$oid'] in labels_map:
        survey = dict(labels_map[composite_trip['_id']['$oid']]).values()[0]
        return survey['data']['name']
    return None


# @memoize
def generate_summaries(metric_list: dict[str, list[str]], trips: list, _app_config, _labels_map: dict[str, any] = None):
    """
    :param metric_list: dict of metric names to lists of grouping fields, e.g. { 'distance': ['mode_confirm', 'purpose_confirm'] }
    :param trips: list of trips, which may be either confirmed_trips or composite_trips
    :param _app_config: app_config, or partial app_config with 'survey_info' present
    :param _labels_map: map of trip_ids to unprocessed user input labels
    """
    global app_config, labels_map
    app_config = _app_config
    labels_map = _labels_map
    # flatten all the incoming trips (if not already flat)
    trips_flat = [
        util.flatten_db_entry(trip) if 'data' in trip else trip
        for trip in trips
    ]
    # only use: a) confirmed_trips, or b) composite_trips that originated from confirmed_trips
    # (this filters out any composite_trips that originated from confirmed_untrackeds)
    # we can treat all that remain as confirmed_trips
    confirmed_trips = [
        trip for trip in trips_flat
        if trip['key'] == 'analysis/confirmed_trip'
        or trip['origin_key'] == 'analysis/confirmed_trip'
    ]
    # sort trips by start ts
    confirmed_trips.sort(key=lambda trip: trip['start_ts'])

    metric_list = dict(metric_list)
    return {metric[0]: get_summary_for_metric(metric, confirmed_trips) for metric in metric_list.items()}


def value_of_metric_for_trip(metric_name: str, grouping_field: str, trip: dict):
    global app_config
    if metric_name == 'distance':
        return trip['distance']
    elif metric_name == 'count':
        return 1
    elif metric_name == 'duration':
        return trip['duration']
    elif metric_name == 'response_count':
        if grouping_field.endswith('_confirm'):
            return 'responded' if label_for_trip(trip, grouping_field[:-8]) else 'not_responded'
        elif grouping_field == 'survey':
            prompted_survey = emcsc.survey_prompted_for_trip(trip, app_config)
            answered_survey = survey_answered_for_trip(trip)
            return 'responded' if answered_survey == prompted_survey else 'not_responded'
    return None


def get_summary_for_metric(metric: tuple[str, list[str]], confirmed_trips: list):
    """
    :param metric: tuple of metric name and list of grouping fields
    :param confirmed_trips: list of confirmed trips
    :return: a list of dicts, each representing a summary of the metric on one day
    e.g. get_summary_for_metric(('distance', ['mode_confirm', 'purpose_confirm']), confirmed_trips)
      -> [ { 'date': '2024-05-20', 'mode_confirm_bike': 1000, 'mode_confirm_walk': 500, 'purpose_confirm_home': 1500 } ]
    """
    days_of_metrics_data = {}
    for trip in confirmed_trips:
        # for now, we're only grouping by day. First part of ISO date is YYYY-MM-DD
        date = trip['start_fmt_time'].split('T')[0]
        if date not in days_of_metrics_data:
            days_of_metrics_data[date] = []
        days_of_metrics_data[date].append(trip)
    # days_summaries e.g. [ { 'date': '2024-05-20', 'mode_confirm_bike': 1000, 'purpose_confirm_home': 1500 } ]
    days_summaries = []
    for date, trips in days_of_metrics_data.items():
        summary_for_day = {
            'date': date,
            'nUsers': len({o['user_id']: 1 for o in trips}),
        }
        summary_for_day.update(metric_summary_for_trips(metric, trips))
        days_summaries.append(summary_for_day)
    return days_summaries


grouping_field_fns = {
    'mode_confirm': lambda trip: label_for_trip(trip, 'mode') or 'UNLABELED',
    'purpose_confirm': lambda trip: label_for_trip(trip, 'purpose') or 'UNLABELED',
    'replaced_mode_confirm': lambda trip: label_for_trip(trip, 'replaced_mode') or 'UNLABELED',
    'survey': lambda trip: emcsc.survey_prompted_for_trip(trip, app_config),
    # 'primary_inferred_mode', maybe add later
    'primary_ble_sensed_mode': lambda trip: emcble.primary_ble_sensed_mode_for_trip(trip) or 'UNKNOWN',
}


def metric_summary_for_trips(metric: tuple[str, list[str]], confirmed_trips: list):
    """
    :param metric: tuple of metric name and list of grouping fields
    :param confirmed_trips: list of confirmed trips
    :return: a dict of { groupingfield_value : metric_total } for the given metric and trips
    e.g. metric_summary_for_trips(('distance', ['mode_confirm', 'purpose_confirm']), confirmed_trips)
      -> { 'mode_confirm_bike': 1000, 'mode_confirm_walk': 500, 'purpose_confirm_home': 1500 }
    e.g. metric_summary_for_trips(('response_count', ['mode_confirm', 'purpose_confirm']), confirmed_trips)
      -> { 'mode_confirm_bike': { 'responded': 10, 'not_responded': 5 }, 'mode_confirm_walk': { 'responded': 5, 'not_responded': 10 } }
    """
    global app_config
    groups = {}
    if not confirmed_trips:
        return groups
    for trip in confirmed_trips:
        if 'primary_ble_sensed_mode' not in trip:
            trip['primary_ble_sensed_mode'] = emcble.primary_ble_sensed_mode_for_trip(
                trip) or 'UNKNOWN'
        for grouping_field in metric[1]:
            if grouping_field not in grouping_field_fns:
                continue
            field_value_for_trip = grouping_field_fns[grouping_field](trip)
            if field_value_for_trip is None:
                continue
            # grouping_key e.g. 'mode_confirm_bike'
            grouping_key = grouping_field + '_' + field_value_for_trip
            val = value_of_metric_for_trip(metric[0], grouping_field, trip)
            # if it's a number, we're summing and adding to the total (used for distance, duration, count)
            if type(val) == int or type(val) == float:
                if grouping_key not in groups:
                    groups[grouping_key] = 0
                groups[grouping_key] += val
            # if it's a string, we're counting the number of times it appears (used for response_count)
            elif type(val) == str:
                if grouping_key not in groups:
                    groups[grouping_key] = {}
                if val not in groups[grouping_key]:
                    groups[grouping_key][val] = 0
                groups[grouping_key][val] += 1
    return groups
