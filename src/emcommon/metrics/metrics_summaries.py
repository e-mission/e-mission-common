from __future__ import annotations  # __: skip
# from util import memoize
import time
import emcommon.logger as Log
import emcommon.util as util
import emcommon.bluetooth.ble_matching as emcble
import emcommon.survey.conditional_surveys as emcsc
import emcommon.metrics.footprint.footprint_calculations as emcmff
import emcommon.metrics.footprint.util as emcmfu
import emcommon.diary.base_modes as emcdb
import emcommon.diary.util as emcdu

app_config = None
labels_map = None

# @memoize


async def generate_summaries(
    metric_list: dict[str, list[str]],
    trips: list,
    _app_config=None,
    _labels_map: dict[str, any] = None,
) -> dict[str, list[dict[str, any]]]:
    """
    :param metric_list: dict of metric names to lists of dimensions, e.g. { 'distance': ['mode_confirm', 'purpose_confirm'] }
    :param trips: list of trips, which may be either confirmed_trips or composite_trips
    :param _app_config: app_config, or partial app_config with 'survey_info' present
    :param _labels_map: map of trip_ids to unprocessed user input labels
    :return: a list of dicts, each representing a summary of a metric on one day
    """
    global app_config, labels_map
    app_config = _app_config
    labels_map = _labels_map
    # flatten all the incoming trips (if not already flat)
    trips_flat = [
        util.flatten_db_entry(trip) if 'data' in trip else trip
        for trip in trips
    ]
    # only use: a) confirmed_trips, or b) composite_trips that originated from *_trip
    # Allows unprocessed trips from the phone (which have origin_key of UNPROCESSED_trip)
    # to be included, but filters out any composite_trips that originated from confirmed_untrackeds.
    # We can treat all that remain as confirmed_trips
    confirmed_trips = [
        trip for trip in trips_flat
        if trip['key'] == 'analysis/confirmed_trip'
        or trip['origin_key'].endswith('_trip')
    ]
    # sort trips by start ts
    confirmed_trips.sort(key=lambda trip: trip['start_ts'])

    metric_list = dict(metric_list)
    summaries = []
    for metric in metric_list.items():
        summaries_for_metric = await get_summary_for_metric(metric, confirmed_trips)
        summaries.extend(summaries_for_metric)
    return summaries


async def value_of_metric_for_trip(metric_name: str, dimension: str, dimension_val: str, trip: dict):
    global app_config, labels_map
    if metric_name == 'distance':
        return trip['distance']
    elif metric_name == 'count':
        return 1
    elif metric_name == 'duration':
        return trip['duration']
    elif metric_name == 'response_count':
        if dimension == 'survey':
            prompted_survey = emcsc.survey_prompted_for_trip(trip, app_config)
            answered_survey = emcdu.survey_answered_for_trip(trip, labels_map)
            return 'responded' if answered_survey == prompted_survey else 'not_responded'
        else:
            if dimension_val == 'UNKNOWN' or dimension_val == 'UNLABELED':
                return 'not_responded'
            return 'responded'
    elif metric_name == 'footprint':
        (footprint, metadata) = await emcmff.calc_footprint_for_trip(trip,
                                                                     app_config['label_options'],
                                                                     'mode',
                                                                     dimension_val,
                                                                     labels_map)
        footprint.update({'metadata': metadata})
        return footprint
    return None


def acc_value_of_metric(metric_name: str, acc, new_val):
    if metric_name == 'distance' or metric_name == 'duration' or metric_name == 'count':
        acc = acc or 0
        return acc + new_val
    elif metric_name == 'response_count':
        acc = acc or {}
        if new_val not in acc:
            acc[new_val] = 0
        acc[new_val] += 1
        return acc
    elif metric_name == 'footprint':
        acc = acc or {'metadata': {}}
        new_val = dict(new_val)
        for key in new_val.keys():
            if key == 'metadata':
                emcmfu.merge_metadatas(acc['metadata'], new_val[key])
            else:
                acc[key] = acc.get(key, 0) + new_val[key]
        return acc


async def get_summary_for_metric(metric: tuple[str, list[str]], confirmed_trips: list):
    """
    :param metric: tuple of metric name and list of dimensions
    :param confirmed_trips: list of confirmed trips
    :return: a list of dicts, each representing a summary of the metric on one day
        e.g. get_summary_for_metric(('distance', ['mode_confirm', 'purpose_confirm']), confirmed_trips) 
        [{
            'date': '2024-05-20',
            'metric': 'distance',
            'nUsers': 2,
            'dimensions': {
                'mode_confirm': { 'value': 'bike', 'measure': 1000 },
                'purpose_confirm': { 'value': 'home', 'measure': 1500 }
            },
            'last_updated': 1747155305,
        }]
    """
    days_of_metrics_data = {}
    for trip in confirmed_trips:
        # for now, we're only grouping by day. First part of ISO date is YYYY-MM-DD
        date = trip['start_fmt_time'].split('T')[0]
        if date not in days_of_metrics_data:
            days_of_metrics_data[date] = []
        days_of_metrics_data[date].append(trip)
    days_summaries = []
    for date, trips in days_of_metrics_data.items():
        summary_for_day = {
            'date': date,
            'metric': metric[0],
            'nUsers': len({o['user_id']: 1 for o in trips}),
            'dimensions': await metric_dimensions_for_trips(metric, trips),
            'last_updated': int(time.time()),
        }
        days_summaries.append(summary_for_day)
    return days_summaries


dimensions_fns = {
    'mode_confirm': lambda trip: emcdu.label_for_trip(trip, 'mode', labels_map) or 'UNLABELED',
    'purpose_confirm': lambda trip: emcdu.label_for_trip(trip, 'purpose', labels_map) or 'UNLABELED',
    'replaced_mode_confirm': lambda trip: emcdu.label_for_trip(trip, 'replaced_mode', labels_map) or 'UNLABELED',
    'survey': lambda trip: emcsc.survey_prompted_for_trip(trip, app_config),
    # 'primary_inferred_mode', maybe add later
    'primary_ble_sensed_mode': lambda trip: emcble.primary_ble_sensed_mode_for_trip(trip) or 'UNKNOWN',
    'mode': lambda trip: emcdu.primary_mode_for_trip(trip, labels_map) or 'UNKNOWN',
}


async def metric_dimensions_for_trips(metric: tuple[str, list[str]], confirmed_trips: list):
    """
    :param metric: tuple of metric name and list of dimensions
    :param confirmed_trips: list of confirmed trips
    :return: a dict of { dimension: [ { "value": "foo", "measure": 0 } ] } for the given metric and trips
    e.g. metric_dimensions_for_trips(('distance', ['mode_confirm', 'purpose_confirm']), confirmed_trips)
      -> { 'mode_confirm_bike': 1000, 'mode_confirm_walk': 500, 'purpose_confirm_home': 1500 }
    e.g. metric_dimensions_for_trips(('response_count', ['mode_confirm', 'purpose_confirm']), confirmed_trips)
      -> { 'mode_confirm_bike': { 'responded': 10, 'not_responded': 5 }, 'mode_confirm_walk': { 'responded': 5, 'not_responded': 10 } }
    """
    global app_config
    dimensions = {}
    if not confirmed_trips:
        return dimensions
    for trip in confirmed_trips:
        if 'primary_ble_sensed_mode' not in trip:
            trip['primary_ble_sensed_mode'] = emcble.primary_ble_sensed_mode_for_trip(
                trip) or 'UNKNOWN'
        for dimension in metric[1]:
            if dimension not in dimensions_fns:
                continue
            dimension_value_for_trip = dimensions_fns[dimension](trip)
            if dimension_value_for_trip is None:
                continue
            if dimension not in dimensions:
                dimensions[dimension] = []

            existing = None
            for d in dimensions[dimension]:
                if d['value'] == dimension_value_for_trip:
                    existing = d
                    break
            measure_for_trip = await value_of_metric_for_trip(metric[0], dimension, dimension_value_for_trip, trip)
            measure = acc_value_of_metric(metric[0],
                                          existing['measure'] if existing else None,
                                          measure_for_trip)
            if existing is None:
                dimensions[dimension].append({
                    'value': dimension_value_for_trip,
                    'measure': measure
                })
            else:
                existing['measure'] = measure
    return dimensions


def munge_agg_metrics(metrics_days):
    """
    Backwards compat to get summaries into the old format that the phone expects in May 2025
    After phone changes and waiting a few months, we can remove this
    """
    munged_result = {}
    for metric_day in metrics_days:
        metric = metric_day['metric']
        if metric not in munged_result:
            munged_result[metric] = []
        munged_summary = {
            'date': metric_day['date'],
            'nUsers': metric_day['nUsers'],
        }
        print(f"metric_day: {metric_day}")
        for dimension in metric_day['dimensions'].keys():
            for dimension_value in metric_day['dimensions'][dimension]:
                munged_summary[f"{dimension}_{dimension_value['value']}"] = dimension_value['measure']
        munged_result[metric].append(munged_summary)
    return munged_result
