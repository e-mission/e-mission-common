from __future__ import annotations  # __: skip
import emcommon.logger as Log
from emcommon.survey.conditional_surveys import survey_prompted_for_trip


# def get_surveys_summary(composite_trips: list, trip_labels_map: dict[str, any], app_config: dict) -> dict:
#     """
#     :param composite_trips: composite trips
#     :return: a summary of the surveys answered for the given composite trips
#     """
#     surveys_summary = {}
#     for trip in composite_trips:
#         prompted_survey = survey_prompted_for_trip(trip, app_config)
#         if not prompted_survey:
#             pass
#             # __pragma__('js', '{}', 'continue;')
#         if prompted_survey not in surveys_summary:
#             surveys_summary[prompted_survey] = {
#                 'answered': 0,
#                 'unanswered': 0,
#                 'mismatched': 0,
#             }
#         answered_survey = survey_answered_for_trip(trip, trip_labels_map)
#         if answered_survey == prompted_survey:
#             surveys_summary[prompted_survey]['answered'] += 1
#         elif answered_survey:
#             Log.warn(f"Unexpected: trip {trip['_id']['$oid']} answered survey {answered_survey} but should have been prompted for {prompted_survey}")
#             surveys_summary[prompted_survey]['mismatched'] += 1
#         else:
#             surveys_summary[prompted_survey]['unanswered'] += 1
#     return surveys_summary


# def get_response_rate_rankings(composite_trips: list, trip_labels_map: dict[str, any], app_config: dict) -> dict:
#     """
#     :param composite_trips: a list of composite trips from multiple users
#     :return: a dict of user_id to response rate, sorted by highest response rate
#     """
#     # bin trips by user_id
#     user_trips = {}
#     for trip in composite_trips:
#         user_id = trip['user_id']
#         if user_id not in user_trips:
#             user_trips[user_id] = []
#         user_trips[user_id].append(trip)
#     # get response rates for each user
#     response_rates = {}
#     for user_id, trips in user_trips.items():
#         summary = get_surveys_summary(trips, trip_labels_map, app_config)
#         answered = sum([s['answered'] for s in summary.values()])
#         unanswered = sum([s['unanswered'] for s in summary.values()])
#         response_rates[user_id] = answered / (answered + unanswered)
#     # sort by highest response rate and return
#     return sorted(response_rates.items(), key=lambda x: x[1], reverse=True)


# def get_median_response_rates(composite_trips: list, trip_labels_map: dict[str, any], app_config: dict) -> dict:
#     # bin trips by user_id
#     user_vals = {}
#     for trip in composite_trips:
#         user_id = trip['user_id']
#         if user_id not in user_vals:
#             user_vals[user_id] = []
#         user_vals[user_id].append(trip)
#     # get response rates for each user
#     response_rates = {}
#     for user_id, trips in user_vals.items():
#         summary = get_surveys_summary(trips, trip_labels_map, app_config)
#         for survey_name, s in summary.items():
#             response_rates[survey_name] = response_rates[survey_name] or []
#             response_rates[survey_name].append(s['answered'] / (s['answered'] + s['unanswered']))

#     # get the median
#     response_rates.sort()
#     median = response_rates[len(response_rates) // 2]
#     return median
