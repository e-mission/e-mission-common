// Transcrypt'ed from Python, 2024-08-27 12:55:27
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as emcmfu from './emcommon.metrics.footprint.util.js';
import * as emcmft from './emcommon.metrics.footprint.transit.js';
import * as emcmfe from './emcommon.metrics.footprint.egrid.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as Log from './emcommon.logger.js';
export {emcmft, emcmfe, emcmfu, Log, emcdb};
var __name__ = 'emcommon.metrics.footprint.footprint_calculations';
export var merge_metadatas = function (meta_a, meta_b) {
	for (var key in meta_b) {
		var value = meta_b [key];
		if (!__in__ (key, meta_a)) {
			meta_a [key] = value;
		}
		else if (hasattr (meta_a [key], 'concat')) {
			meta_a [key] = meta_a [key].concat (value);
		}
		else if (isinstance (value, list)) {
			meta_a [key] = meta_a [key] + value;
		}
		else if (isinstance (value, bool)) {
			meta_a [key] = meta_a [key] || value;
		}
		else {
			meta_a [key] = value;
		}
	}
};
export var calc_footprint_for_trip = async function (trip, mode_label_option) {
	Log.debug ((('Getting footprint for trip: ' + str (trip)) + ', with mode option: ') + str (mode_label_option));
	var metadata = dict ({});
	var distance = trip ['distance'];
	var rich_mode = emcdb.get_rich_mode (mode_label_option);
	var mode_footprint = dict (rich_mode ['footprint']);
	if (__in__ ('transit', mode_footprint)) {
		var __left0__ = await emcmft.get_transit_intensities_for_trip (trip, mode_footprint ['transit']);
		var mode_footprint = __left0__ [0];
		var transit_metadata = __left0__ [1];
		merge_metadatas (metadata, transit_metadata);
	}
	var kwh_total = 0;
	var kg_co2_total = 0;
	for (var fuel_type in mode_footprint) {
		var fuel_type_footprint = mode_footprint [fuel_type];
		var kwh = ((distance / 1000) * fuel_type_footprint ['wh_per_km']) / 1000;
		if (__in__ (fuel_type, emcmfu.FUELS_KG_CO2_PER_KWH)) {
			Log.debug ('Using default carbon intensity for fuel type: ' + fuel_type);
			var kg_co2 = kwh * emcmfu.FUELS_KG_CO2_PER_KWH [fuel_type];
		}
		else if (fuel_type == 'electric') {
			Log.debug ('Using eGRID carbon intensity for electric');
			var __left0__ = await emcmfe.get_egrid_intensity_for_trip (trip);
			var kg_per_kwh = __left0__ [0];
			var egrid_metadata = __left0__ [1];
			merge_metadatas (metadata, egrid_metadata);
			var kg_co2 = kwh * kg_per_kwh;
		}
		else {
			Log.warn ('Unknown fuel type: ' + fuel_type);
			continue;
		}
		kwh_total += kwh;
		kg_co2_total += kg_co2;
	}
	var passengers = (__in__ ('passengers', mode_label_option) ? mode_label_option ['passengers'] : 1);
	var footprint = dict ({'kwh': kwh_total / passengers, 'kg_co2': kg_co2_total / passengers});
	return tuple ([footprint, metadata]);
};

//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.map