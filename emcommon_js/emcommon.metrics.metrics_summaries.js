// Transcrypt'ed from Python, 2024-09-25 01:43:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as emcdu from './emcommon.diary.util.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as emcmfu from './emcommon.metrics.footprint.util.js';
import * as emcmff from './emcommon.metrics.footprint.footprint_calculations.js';
import * as emcsc from './emcommon.survey.conditional_surveys.js';
import * as emcble from './emcommon.bluetooth.ble_matching.js';
import * as util from './emcommon.util.js';
import * as Log from './emcommon.logger.js';
export {emcmfu, Log, emcsc, util, emcdu, emcmff, emcble, emcdb};
var __name__ = 'emcommon.metrics.metrics_summaries';
export var app_config = null;
export var labels_map = null;
export var generate_summaries = async function (metric_list, trips, _app_config, _labels_map) {
	if (typeof _app_config == 'undefined' || (_app_config != null && _app_config.hasOwnProperty ("__kwargtrans__"))) {;
		_app_config = null;
	};
	if (typeof _labels_map == 'undefined' || (_labels_map != null && _labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		_labels_map = null;
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
			if (trip ['key'] == 'analysis/confirmed_trip' || trip ['origin_key'].endswith ('_trip')) {
				__accu0__.append (trip);
			}
		}
		return __accu0__;
	}) ();
	confirmed_trips.py_sort (__kwargtrans__ ({key: (function __lambda__ (trip) {
		return trip ['start_ts'];
	})}));
	metric_list = dict (metric_list);
	var summaries = dict ({});
	for (var metric of metric_list.py_items ()) {
		summaries [metric [0]] = await get_summary_for_metric (metric, confirmed_trips);
	}
	return summaries;
};
export var value_of_metric_for_trip = async function (metric_name, grouping_field, grouping_val, trip) {
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
		if (grouping_field == 'survey') {
			var prompted_survey = emcsc.survey_prompted_for_trip (trip, app_config);
			var answered_survey = emcdu.survey_answered_for_trip (trip, labels_map);
			return (answered_survey == prompted_survey ? 'responded' : 'not_responded');
		}
		else {
			if (grouping_val == 'UNKNOWN' || grouping_val == 'UNLABELED') {
				return 'not_responded';
			}
			return 'responded';
		}
	}
	else if (metric_name == 'footprint') {
		var __left0__ = await emcmff.calc_footprint_for_trip (trip, app_config ['label_options'], 'mode', grouping_val, labels_map);
		var footprint = __left0__ [0];
		var metadata = __left0__ [1];
		footprint.py_update (dict ({'metadata': metadata}));
		return footprint;
	}
	return null;
};
export var acc_value_of_metric = function (metric_name, acc, new_val) {
	if (metric_name == 'distance' || metric_name == 'duration' || metric_name == 'count') {
		acc = acc || 0;
		return acc + new_val;
	}
	else if (metric_name == 'response_count') {
		acc = acc || dict ({});
		if (!__in__ (new_val, acc)) {
			acc [new_val] = 0;
		}
		acc [new_val]++;
		return acc;
	}
	else if (metric_name == 'footprint') {
		acc = acc || dict ({'metadata': dict ({})});
		new_val = dict (new_val);
		for (var key of new_val.py_keys ()) {
			if (key == 'metadata') {
				emcmfu.merge_metadatas (acc ['metadata'], new_val [key]);
			}
			else {
				acc [key] = acc.py_get (key, 0) + new_val [key];
			}
		}
		return acc;
	}
};
export var get_summary_for_metric = async function (metric, confirmed_trips) {
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
		summary_for_day.py_update (await metric_summary_for_trips (metric, trips));
		days_summaries.append (summary_for_day);
	}
	return days_summaries;
};
export var grouping_field_fns = dict ({'mode_confirm': (function __lambda__ (trip) {
	return emcdu.label_for_trip (trip, 'mode', labels_map) || 'UNLABELED';
}), 'purpose_confirm': (function __lambda__ (trip) {
	return emcdu.label_for_trip (trip, 'purpose', labels_map) || 'UNLABELED';
}), 'replaced_mode_confirm': (function __lambda__ (trip) {
	return emcdu.label_for_trip (trip, 'replaced_mode', labels_map) || 'UNLABELED';
}), 'survey': (function __lambda__ (trip) {
	return emcsc.survey_prompted_for_trip (trip, app_config);
}), 'primary_ble_sensed_mode': (function __lambda__ (trip) {
	return emcble.primary_ble_sensed_mode_for_trip (trip) || 'UNKNOWN';
}), 'mode': (function __lambda__ (trip) {
	return emcdu.primary_mode_for_trip (trip, labels_map) || 'UNKNOWN';
})});
export var metric_summary_for_trips = async function (metric, confirmed_trips) {
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
			var val = await value_of_metric_for_trip (metric [0], grouping_field, field_value_for_trip, trip);
			groups [grouping_key] = acc_value_of_metric (metric [0], groups.py_get (grouping_key), val);
		}
	}
	return groups;
};

//# sourceMappingURL=emcommon.metrics.metrics_summaries.map