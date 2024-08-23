# This is the entry point for Transcrypt, specifying the Python code that will be transpiled to JavaScript

import emcommon.logger as Logger
import emcommon.metrics.metrics_summaries as metrics_summaries
# import emcommon.metrics.surveys.surveys_summary as surveys_summary
import emcommon.metrics.active_travel.active_travel_calculations as active_travel_calculations
import emcommon.survey.conditional_surveys as conditional_surveys
import emcommon.bluetooth.ble_matching as ble_matching
import emcommon.metrics.footprint.footprint_calculations as footprint_calculations
import emcommon.diary.base_modes as base_modes


# Add methods from Transcrypt's 'dict' to the JS Object prototype,
# allowing emcommon to use JS objects the same way it uses Python dicts
'''?
d = dict()
for p in Object.getOwnPropertyNames(d.__proto__ if d.__proto__.__class__ else d):
    d['value'] = d[p]
    __setproperty__(Object.prototype, p, d)
?'''
