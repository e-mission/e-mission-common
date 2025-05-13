// Transcrypt'ed from Python, 2025-05-13 19:52:13
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as emcmfu from './emcommon.metrics.footprint.util.js';
import * as emcmft from './emcommon.metrics.footprint.transit.js';
import * as emcmfe from './emcommon.metrics.footprint.egrid.js';
import * as emcdu from './emcommon.diary.util.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as Log from './emcommon.logger.js';
export {emcmft, emcdb, Log, emcdu, emcmfe, emcmfu};
var __name__ = 'emcommon.metrics.footprint.footprint_calculations';
export var calc_footprint_for_trip = async function (trip, label_options, mode_key, mode_value, labels_map) {
	if (typeof mode_key == 'undefined' || (mode_key != null && mode_key.hasOwnProperty ("__kwargtrans__"))) {;
		mode_key = 'mode';
	};
	if (typeof mode_value == 'undefined' || (mode_value != null && mode_value.hasOwnProperty ("__kwargtrans__"))) {;
		mode_value = null;
	};
	if (typeof labels_map == 'undefined' || (labels_map != null && labels_map.hasOwnProperty ("__kwargtrans__"))) {;
		labels_map = null;
	};
	trip = dict (trip);
	mode_value = mode_value || emcdu.label_for_trip (trip, mode_key, labels_map);
	var rich_mode = mode_value && emcdb.get_rich_mode_for_value (mode_value, label_options);
	var is_uncertain = false;
	if (rich_mode === null || !__in__ ('footprint', rich_mode)) {
		var is_uncertain = true;
		var rich_mode = find_worst_rich_mode (label_options);
	}
	var __left0__ = await calc_footprint (rich_mode ['footprint'], trip ['distance'], emcmfu.year_of_trip (trip), trip ['start_loc'] ['coordinates'], trip.py_get ('uace_region'), trip.py_get ('egrid_region'), rich_mode.py_get ('passengers', 1), dict ({'trip_id': trip ['_id']}));
	var footprint = __left0__ [0];
	var metadata = __left0__ [1];
	if (is_uncertain) {
		footprint ['kwh_uncertain'] = footprint ['kwh'];
		footprint ['kg_co2_uncertain'] = footprint ['kg_co2'];
		footprint ['kwh'] = 0;
		footprint ['kg_co2'] = 0;
	}
	return tuple ([footprint, metadata]);
};
export var calc_footprint = async function (mode_footprint, distance, year, coords, uace, egrid_region, passengers, metadata) {
	if (typeof uace == 'undefined' || (uace != null && uace.hasOwnProperty ("__kwargtrans__"))) {;
		uace = null;
	};
	if (typeof egrid_region == 'undefined' || (egrid_region != null && egrid_region.hasOwnProperty ("__kwargtrans__"))) {;
		egrid_region = null;
	};
	if (typeof passengers == 'undefined' || (passengers != null && passengers.hasOwnProperty ("__kwargtrans__"))) {;
		passengers = 1;
	};
	if (typeof metadata == 'undefined' || (metadata != null && metadata.hasOwnProperty ("__kwargtrans__"))) {;
		metadata = dict ({});
	};
	mode_footprint = dict (mode_footprint);
	if (__in__ ('transit', mode_footprint)) {
		var __left0__ = await emcmft.get_transit_intensities (year, coords, uace, mode_footprint ['transit']);
		mode_footprint = __left0__ [0];
		var transit_metadata = __left0__ [1];
		emcmfu.merge_metadatas (metadata, transit_metadata);
	}
	var kwh_total = 0;
	var kg_co2_total = 0;
	for (var fuel_type of mode_footprint.py_keys ()) {
		var fuel_type_footprint = mode_footprint [fuel_type];
		var kwh = 0;
		if (__in__ ('wh_per_km', fuel_type_footprint)) {
			kwh += ((distance / 1000) * fuel_type_footprint ['wh_per_km']) / 1000;
		}
		if (__in__ ('wh_per_trip', fuel_type_footprint)) {
			kwh += fuel_type_footprint ['wh_per_trip'] / 1000;
		}
		if (__in__ (fuel_type, emcmfu.FUELS_KG_CO2_PER_MWH)) {
			var kg_co2 = (kwh / 1000) * emcmfu.FUELS_KG_CO2_PER_MWH [fuel_type];
		}
		else if (fuel_type == 'electric') {
			var __left0__ = await emcmfe.get_egrid_intensity (year, coords, egrid_region);
			var kg_per_mwh = __left0__ [0];
			var egrid_metadata = __left0__ [1];
			emcmfu.merge_metadatas (metadata, egrid_metadata);
			var kg_co2 = (kwh * kg_per_mwh) / 1000;
		}
		else if (fuel_type != 'overall') {
			Log.warn ('Unknown fuel type: ' + fuel_type);
			continue;
		}
		var weight = (__in__ ('weight', fuel_type_footprint) ? fuel_type_footprint ['weight'] : 1);
		kwh_total += kwh * weight;
		kg_co2_total += kg_co2 * weight;
	}
	var footprint = dict ({'kwh': kwh_total / passengers, 'kg_co2': kg_co2_total / passengers});
	return tuple ([footprint, metadata]);
};
export var _worst_rich_mode = null;
export var _worst_wh_per_km = 0;
export var find_worst_rich_mode = function (label_options) {
	if (_worst_rich_mode !== null) {
		return _worst_rich_mode;
	}
	for (var opt of label_options ['MODE']) {
		var rm = emcdb.get_rich_mode (opt);
		if (!__in__ ('footprint', rm) || __in__ ('transit', rm ['footprint'])) {
			continue;
		}
		var mode_footprint = dict (rm ['footprint']);
		for (var fuel_type of mode_footprint.py_keys ()) {
			if (__in__ ('wh_per_km', rm ['footprint'] [fuel_type])) {
				var wh_per_km = rm ['footprint'] [fuel_type] ['wh_per_km'];
				if (wh_per_km > _worst_wh_per_km) {
					_worst_rich_mode = rm;
					_worst_wh_per_km = wh_per_km;
				}
			}
		}
	}
	Log.debug ('Worst rich mode is {} with {} wh_per_km'.format (str (_worst_rich_mode ['value']), str (_worst_wh_per_km)));
	return _worst_rich_mode;
};

//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.map