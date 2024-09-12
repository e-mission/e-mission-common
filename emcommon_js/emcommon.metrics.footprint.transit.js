// Transcrypt'ed from Python, 2024-08-31 02:04:27
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as util from './emcommon.metrics.footprint.util.js';
import * as Log from './emcommon.logger.js';
export {Log, util};
var __name__ = 'emcommon.metrics.footprint.transit';
export var fuel_types = ['Gasoline', 'Diesel', 'LPG', 'CNG', 'Hydrogen', 'Electric', 'Other'];
export var weighted_mean = function (py_values, weights) {
	var w_sum = sum (weights);
	return sum ((function () {
		var __accu0__ = [];
		for (var [v, w] of zip (py_values, weights)) {
			__accu0__.append ((v * w) / w_sum);
		}
		return __accu0__;
	}) ());
};
export var get_transit_intensities = async function (year, coords, uace, modes, metadata) {
	if (typeof coords == 'undefined' || (coords != null && coords.hasOwnProperty ("__kwargtrans__"))) {;
		var coords = null;
	};
	if (typeof uace == 'undefined' || (uace != null && uace.hasOwnProperty ("__kwargtrans__"))) {;
		var uace = null;
	};
	if (typeof modes == 'undefined' || (modes != null && modes.hasOwnProperty ("__kwargtrans__"))) {;
		var modes = null;
	};
	if (typeof metadata == 'undefined' || (metadata != null && metadata.hasOwnProperty ("__kwargtrans__"))) {;
		var metadata = dict ({});
	};
	if (uace === null) {
		metadata.py_update (dict ({'requested_coords': coords}));
		var uace = await util.get_uace_by_coords (coords, year);
	}
	return await get_transit_intensities_for_uace (year, uace, modes, metadata);
};
export var get_transit_intensities_for_uace = async function (year, uace, modes, metadata) {
	if (typeof uace == 'undefined' || (uace != null && uace.hasOwnProperty ("__kwargtrans__"))) {;
		var uace = null;
	};
	if (typeof modes == 'undefined' || (modes != null && modes.hasOwnProperty ("__kwargtrans__"))) {;
		var modes = null;
	};
	if (typeof metadata == 'undefined' || (metadata != null && metadata.hasOwnProperty ("__kwargtrans__"))) {;
		var metadata = dict ({});
	};
	var intensities_data = await util.get_intensities_data (year, 'ntd');
	var actual_year = intensities_data ['metadata'] ['year'];
	metadata.py_update (dict ({'data_sources': ['ntd{}'.format (actual_year)], 'data_source_urls': intensities_data ['metadata'] ['data_source_urls'], 'is_provisional': actual_year != year, 'requested_year': year, 'ntd_uace_code': uace, 'ntd_modes': modes, 'ntd_ids': []}));
	var total_upt = 0;
	var agency_mode_fueltypes = [];
	for (var entry of intensities_data ['records']) {
		if (modes && !__in__ (entry ['Mode'], modes) || uace && entry ['UACE Code'] != uace) {
			continue;
		}
		var upt = entry ['Unlinked Passenger Trips'];
		total_upt += upt;
		for (var fuel_type of fuel_types) {
			var fuel_pct = (__in__ ('{} (%)'.format (fuel_type), entry) ? entry ['{} (%)'.format (fuel_type)] : 0);
			var wh_per_pkm = (__in__ ('{} (Wh/pkm)'.format (fuel_type), entry) ? entry ['{} (Wh/pkm)'.format (fuel_type)] : 0);
			if (fuel_pct && wh_per_pkm) {
				agency_mode_fueltypes.append (dict ({'fuel_type': fuel_type, 'upt': (fuel_pct / 100) * upt, 'wh_per_km': wh_per_pkm}));
				if (!__in__ (entry ['NTD ID'], metadata ['ntd_ids'])) {
					metadata ['ntd_ids'].append (entry ['NTD ID']);
				}
			}
		}
	}
	if (!(agency_mode_fueltypes)) {
		if (uace) {
			Log.info ('Insufficient data for year {} and UACE {} and modes {}. Retrying with UACE=None'.format (year, uace, modes));
			return await get_transit_intensities_for_uace (year, null, modes);
		}
		if (modes) {
			Log.info ('Insufficient data for year {} and UACE {} and modes {}. Retrying with modes = None'.format (year, uace, modes));
			return await get_transit_intensities_for_uace (year, uace, null);
		}
		Log.error ('No data available for any UACE or modes');
		return tuple ([null, metadata]);
	}
	for (var entry of agency_mode_fueltypes) {
		entry ['weight'] = entry ['upt'] / total_upt;
	}
	var intensities = dict ({});
	for (var fuel_type of fuel_types) {
		var fuel_type_entries = (function () {
			var __accu0__ = [];
			for (var entry of agency_mode_fueltypes) {
				if (entry ['fuel_type'] == fuel_type) {
					__accu0__.append (entry);
				}
			}
			return __accu0__;
		}) ();
		if (len (fuel_type_entries) == 0) {
			continue;
		}
		var wh_per_km_values = (function () {
			var __accu0__ = [];
			for (var entry of fuel_type_entries) {
				__accu0__.append (entry ['wh_per_km']);
			}
			return __accu0__;
		}) ();
		var weights = (function () {
			var __accu0__ = [];
			for (var entry of fuel_type_entries) {
				__accu0__.append (entry ['weight']);
			}
			return __accu0__;
		}) ();
		var fuel_type = fuel_type.lower ();
		intensities [fuel_type] = dict ({'wh_per_km': weighted_mean (wh_per_km_values, weights), 'weight': sum (weights)});
	}
	var wh_per_km_values = (function () {
		var __accu0__ = [];
		for (var entry of agency_mode_fueltypes) {
			__accu0__.append (entry ['wh_per_km']);
		}
		return __accu0__;
	}) ();
	var weights = (function () {
		var __accu0__ = [];
		for (var entry of agency_mode_fueltypes) {
			__accu0__.append (entry ['weight']);
		}
		return __accu0__;
	}) ();
	intensities ['overall'] = dict ({'wh_per_km': weighted_mean (wh_per_km_values, weights), 'weight': sum (weights)});
	return tuple ([intensities, metadata]);
};

//# sourceMappingURL=emcommon.metrics.footprint.transit.map