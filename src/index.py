# This is the entry point for Transcrypt, specifying the Python code that will be transpiled to JavaScript

import emcommon.logger as Log
import emcommon.metrics.metrics_summaries as metrics_summaries
# import emcommon.metrics.surveys.surveys_summary as surveys_summary
import emcommon.metrics.active_travel.active_travel_calculations as active_travel_calculations
import emcommon.survey.conditional_surveys as conditional_surveys
import emcommon.bluetooth.ble_matching as ble_matching
import emcommon.metrics.footprint.footprint_calculations as footprint_calculations
import emcommon.diary.base_modes as base_modes


def dict_to_js_obj(py_dict):
    """
    Converts a Python dictionary to a JavaScript object
    """
    js_obj = {}  # __: jsiter
    for key, value in py_dict.items():
        if isinstance(value, dict):
            js_obj[key] = dict_to_js_obj(value)
        else:
            js_obj[key] = value
    return js_obj
