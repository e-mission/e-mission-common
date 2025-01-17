// Transcrypt'ed from Python, 2025-01-17 16:17:43
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as emcble from './emcommon.bluetooth.ble_matching.js';
import * as Log from './emcommon.logger.js';
export {emcble, Log};
var __name__ = 'emcommon.diary.util';
export var label_for_trip = function (composite_trip, label_key, labels_map) {
	if (typeof labels_map == 'undefined' || (labels_map != null && labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		labels_map = null;
	};
	label_key = label_key.upper ();
	var label_key_confirm = label_key.lower () + '_confirm';
	if (__in__ ('user_input', composite_trip) && __in__ (label_key_confirm, composite_trip ['user_input'])) {
		return composite_trip ['user_input'] [label_key_confirm];
	}
	if (labels_map && __in__ (composite_trip ['_id'] ['$oid'], labels_map) && __in__ (label_key, labels_map [composite_trip ['_id'] ['$oid']])) {
		return labels_map [composite_trip ['_id'] ['$oid']] [label_key] ['data'] ['label'];
	}
	return null;
};
export var survey_answered_for_trip = function (composite_trip, labels_map) {
	if (typeof labels_map == 'undefined' || (labels_map != null && labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		labels_map = null;
	};
	if (__in__ ('user_input', composite_trip) && __in__ ('trip_user_input', composite_trip ['user_input'])) {
		return composite_trip ['user_input'] ['trip_user_input'] ['data'] ['name'];
	}
	if (labels_map && __in__ (composite_trip ['_id'] ['$oid'], labels_map)) {
		var survey = dict (labels_map [composite_trip ['_id'] ['$oid']]).py_values () [0];
		return survey ['data'] ['name'];
	}
	return null;
};
export var primary_inferred_mode_for_trip = function (trip, labels_map) {
	if (typeof labels_map == 'undefined' || (labels_map != null && labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		labels_map = null;
	};
	return null;
};
export var primary_sensed_mode_for_trip = function (trip) {
	if (!__in__ ('cleaned_section_summary', trip)) {
		return null;
	}
	var dists = dict (trip ['cleaned_section_summary'] ['distance']);
	return max (dists, __kwargtrans__ ({key: dists.py_get}));
};
export var primary_mode_for_trip = function (trip, labels_map) {
	if (typeof labels_map == 'undefined' || (labels_map != null && labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		labels_map = null;
	};
	return label_for_trip (trip, 'mode', labels_map) || emcble.primary_ble_sensed_mode_for_trip (trip) || primary_inferred_mode_for_trip (trip, labels_map) || primary_sensed_mode_for_trip (trip) || null;
};

//# sourceMappingURL=emcommon.diary.util.map