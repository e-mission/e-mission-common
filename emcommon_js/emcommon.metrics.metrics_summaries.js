// Transcrypt'ed from Python, 2024-08-27 12:55:28
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as emcsc from './emcommon.survey.conditional_surveys.js';
import * as emcble from './emcommon.bluetooth.ble_matching.js';
import * as util from './emcommon.util.js';
import * as Log from './emcommon.logger.js';
export {emcsc, emcble, Log, util};
var __name__ = 'emcommon.metrics.metrics_summaries';
export var app_config = null;
export var labels_map = null;
export var label_for_trip = function (composite_trip, label_key) {
	var label_key = label_key.upper ();
	var label_key_confirm = label_key.lower () + '_confirm';
	if (__in__ ('user_input', composite_trip) && __in__ (label_key_confirm, composite_trip ['user_input'])) {
		return composite_trip ['user_input'] [label_key_confirm];
	}
	if (labels_map && __in__ (composite_trip ['_id'] ['$oid'], labels_map) && __in__ (label_key, labels_map [composite_trip ['_id'] ['$oid']])) {
		return labels_map [composite_trip ['_id'] ['$oid']] [label_key] ['data'] ['label'];
	}
	return null;
};
export var survey_answered_for_trip = function (composite_trip) {
	if (__in__ ('user_input', composite_trip) && __in__ ('trip_user_input', composite_trip ['user_input'])) {
		return composite_trip ['user_input'] ['trip_user_input'] ['data'] ['name'];
	}
	if (labels_map && __in__ (composite_trip ['_id'] ['$oid'], labels_map)) {
		var survey = dict (labels_map [composite_trip ['_id'] ['$oid']]).py_values () [0];
		return survey ['data'] ['name'];
	}
	return null;
};
export var generate_summaries = function (metric_list, trips, _app_config, _labels_map) {
	if (typeof _labels_map == 'undefined' || (_labels_map != null && _labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		var _labels_map = null;
	};
	app_config = _app_config;
	labels_map = _labels_map;
	var trips_flat = (function () {
		var __accu0__ = [];
		for (var trip of trips) {
			__accu0__.append ((__in__ ('data', trip) ? util.flatten_db_entry (trip) : trip));
		}
		return __accu0__;
	}) ();
	var confirmed_trips = (function () {
		var __accu0__ = [];
		for (var trip of trips_flat) {
			if (trip ['key'] == 'analysis/confirmed_trip' || trip ['origin_key'] == 'analysis/confirmed_trip') {
				__accu0__.append (trip);
			}
		}
		return __accu0__;
	}) ();
	confirmed_trips.py_sort (__kwargtrans__ ({key: (function __lambda__ (trip) {
		return trip ['start_ts'];
	})}));
	var metric_list = dict (metric_list);
	return (function () {
		var __accu0__ = [];
		for (var metric of metric_list.py_items ()) {
			__accu0__.append ([metric [0], get_summary_for_metric (metric, confirmed_trips)]);
		}
		return dict (__accu0__);
	}) ();
};
export var value_of_metric_for_trip = function (metric_name, grouping_field, trip) {
	if (metric_name == 'distance') {
		return trip ['distance'];
	}
	else if (metric_name == 'count') {
		return 1;
	}
	else if (metric_name == 'duration') {
		return trip ['duration'];
	}
	else if (metric_name == 'response_count') {
		if (grouping_field.endswith ('_confirm')) {
			return (label_for_trip (trip, grouping_field.__getslice__ (0, -(8), 1)) ? 'responded' : 'not_responded');
		}
		else if (grouping_field == 'survey') {
			var prompted_survey = emcsc.survey_prompted_for_trip (trip, app_config);
			var answered_survey = survey_answered_for_trip (trip);
			return (answered_survey == prompted_survey ? 'responded' : 'not_responded');
		}
	}
	return null;
};
export var get_summary_for_metric = function (metric, confirmed_trips) {
	var days_of_metrics_data = dict ({});
	for (var trip of confirmed_trips) {
		var date = trip ['start_fmt_time'].py_split ('T') [0];
		if (!__in__ (date, days_of_metrics_data)) {
			days_of_metrics_data [date] = [];
		}
		days_of_metrics_data [date].append (trip);
	}
	var days_summaries = [];
	for (var [date, trips] of days_of_metrics_data.py_items ()) {
		var summary_for_day = dict ({'date': date, 'nUsers': len ((function () {
			var __accu0__ = [];
			for (var o of trips) {
				__accu0__.append ([o ['user_id'], 1]);
			}
			return dict (__accu0__);
		}) ())});
		summary_for_day.py_update (metric_summary_for_trips (metric, trips));
		days_summaries.append (summary_for_day);
	}
	return days_summaries;
};
export var grouping_field_fns = dict ({'mode_confirm': (function __lambda__ (trip) {
	return label_for_trip (trip, 'mode') || 'UNLABELED';
}), 'purpose_confirm': (function __lambda__ (trip) {
	return label_for_trip (trip, 'purpose') || 'UNLABELED';
}), 'replaced_mode_confirm': (function __lambda__ (trip) {
	return label_for_trip (trip, 'replaced_mode') || 'UNLABELED';
}), 'survey': (function __lambda__ (trip) {
	return emcsc.survey_prompted_for_trip (trip, app_config);
}), 'primary_ble_sensed_mode': (function __lambda__ (trip) {
	return emcble.primary_ble_sensed_mode_for_trip (trip) || 'UNKNOWN';
})});
export var metric_summary_for_trips = function (metric, confirmed_trips) {
	var groups = dict ({});
	if (!(confirmed_trips)) {
		return groups;
	}
	for (var trip of confirmed_trips) {
		if (!__in__ ('primary_ble_sensed_mode', trip)) {
			trip ['primary_ble_sensed_mode'] = emcble.primary_ble_sensed_mode_for_trip (trip) || 'UNKNOWN';
		}
		for (var grouping_field of metric [1]) {
			if (!__in__ (grouping_field, grouping_field_fns)) {
				continue;
			}
			var field_value_for_trip = grouping_field_fns [grouping_field] (trip);
			if (field_value_for_trip === null) {
				continue;
			}
			var grouping_key = (grouping_field + '_') + field_value_for_trip;
			var val = value_of_metric_for_trip (metric [0], grouping_field, trip);
			if (py_typeof (val) == int || py_typeof (val) == float) {
				if (!__in__ (grouping_key, groups)) {
					groups [grouping_key] = 0;
				}
				groups [grouping_key] += val;
			}
			else if (py_typeof (val) == str) {
				if (!__in__ (grouping_key, groups)) {
					groups [grouping_key] = dict ({});
				}
				if (!__in__ (val, groups [grouping_key])) {
					groups [grouping_key] [val] = 0;
				}
				groups [grouping_key] [val]++;
			}
		}
	}
	return groups;
};

//# sourceMappingURL=emcommon.metrics.metrics_summaries.map