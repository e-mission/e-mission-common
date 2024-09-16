// Transcrypt'ed from Python, 2024-09-16 11:51:20
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as Log from './emcommon.logger.js';
export {Log};
var __name__ = 'emcommon.bluetooth.ble_matching';
export var get_ble_sensed_vehicle_for_section = function (ble_entries, start_ts, end_ts, app_config) {
	Log.debug (__mod__ ('getting BLE sensed vehicle for section from %d to %d', tuple ([start_ts, end_ts])));
	if (!__in__ ('vehicle_identities', app_config)) {
		return null;
	}
	var ble_ranging_entries_during_section = get_ble_range_updates_for_section (ble_entries, start_ts, end_ts);
	Log.debug (__mod__ ('After filtering, %d BLE ranging entries during the section', len (ble_ranging_entries_during_section)));
	if (len (ble_ranging_entries_during_section) == 0) {
		return null;
	}
	var ble_beacon_counts = dict ({});
	for (var entry of ble_ranging_entries_during_section) {
		var major_minor = ('{:02x}'.format (entry ['data'] ['major']) + ':') + '{:02x}'.format (entry ['data'] ['minor']);
		if (!__in__ (major_minor, ble_beacon_counts)) {
			ble_beacon_counts [major_minor] = 0;
		}
		ble_beacon_counts [major_minor]++;
	}
	Log.debug (__mod__ ('after counting, ble_beacon_counts = %s', ble_beacon_counts));
	var ble_beacon_major_minor = max (ble_beacon_counts, __kwargtrans__ ({key: ble_beacon_counts.py_get}));
	return get_vehicle_with_ble_beacon (ble_beacon_major_minor, app_config);
};
export var decimal_to_hex_string = function (n, min_length) {
	if (typeof min_length == 'undefined' || (min_length != null && min_length.hasOwnProperty ("__kwargtrans__"))) {;
		min_length = 0;
	};
	var hex = Number (n).toString (16);
	while (len (hex) < min_length) {
		var hex = '0' + hex;
	}
	return hex;
};
export var get_ble_range_updates_for_section = function (ble_entries, start_ts, end_ts) {
	return (function () {
		var __accu0__ = [];
		for (var entry of ble_entries) {
			if (entry ['data'] ['ts'] >= start_ts && entry ['data'] ['ts'] <= end_ts && (entry ['data'] ['eventType'] == 'RANGE_UPDATE' || entry ['data'] ['eventType'] == 2)) {
				__accu0__.append (entry);
			}
		}
		return __accu0__;
	}) ();
};
export var get_vehicle_with_ble_beacon = function (major_minor, app_config) {
	for (var vehicle of app_config ['vehicle_identities']) {
		if (__in__ (major_minor, vehicle ['bluetooth_major_minor'])) {
			Log.debug (__mod__ ('found vehicle %s with BLE beacon %s', tuple ([vehicle ['text'], major_minor])));
			return vehicle;
		}
	}
	Log.debug (__mod__ ('no vehicle found for BLE beacon %s', major_minor));
	return null;
};
export var primary_ble_sensed_mode_for_trip = function (trip) {
	if (!__in__ ('ble_sensed_summary', trip) || !__in__ ('distance', trip ['ble_sensed_summary'])) {
		return null;
	}
	var dists = trip ['ble_sensed_summary'] ['distance'];
	var dists = (py_typeof (dists) == dict ? dists : dict (dists));
	var high = tuple ([null, 0]);
	for (var [k, v] of dists.py_items ()) {
		var high = (v > high [1] ? tuple ([k, v]) : high);
	}
	return high [0];
};

//# sourceMappingURL=emcommon.bluetooth.ble_matching.map