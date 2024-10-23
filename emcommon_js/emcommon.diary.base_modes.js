// Transcrypt'ed from Python, 2024-10-23 19:03:19
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {mpge_to_wh_per_km} from './emcommon.metrics.footprint.util.js';
import * as Log from './emcommon.logger.js';
export {mpge_to_wh_per_km, Log};
var __name__ = 'emcommon.diary.base_modes';
import color from 'color'
export var mode_colors = dict ({'pink': '#c32e85', 'red': '#c21725', 'orange': '#bf5900', 'green': '#008148', 'blue': '#0074b7', 'periwinkle': '#6356bf', 'magenta': '#9240a4', 'grey': '#555555', 'taupe': '#7d585a'});
export var WALKING_METS = dict ({'VERY_SLOW': dict ({'range': [0, 2.0], 'mets': 2.0}), 'SLOW': dict ({'range': [2.0, 2.5], 'mets': 2.8}), 'MODERATE_0': dict ({'range': [2.5, 2.8], 'mets': 3.0}), 'MODERATE_1': dict ({'range': [2.8, 3.2], 'mets': 3.5}), 'FAST': dict ({'range': [3.2, 3.5], 'mets': 4.3}), 'VERY_FAST_0': dict ({'range': [3.5, 4.0], 'mets': 5.0}), 'VERY_FAST_1': dict ({'range': [4.0, 4.5], 'mets': 6.0}), 'VERY_VERY_FAST': dict ({'range': [4.5, 5], 'mets': 7.0}), 'SUPER_FAST': dict ({'range': [5, 6], 'mets': 8.3}), 'RUNNING': dict ({'range': [6, float ('inf')], 'mets': 9.8})});
export var BIKING_METS = dict ({'VERY_VERY_SLOW': dict ({'range': [0, 5.5], 'mets': 3.5}), 'VERY_SLOW': dict ({'range': [5.5, 10], 'mets': 5.8}), 'SLOW': dict ({'range': [10, 12], 'mets': 6.8}), 'MODERATE': dict ({'range': [12, 14], 'mets': 8.0}), 'FAST': dict ({'range': [14, 16], 'mets': 10.0}), 'VERT_FAST': dict ({'range': [16, 19], 'mets': 12.0}), 'RACING': dict ({'range': [20, float ('inf')], 'mets': 15.8})});
export var E_BIKING_METS = dict ({'ALL': dict ({'range': [0, float ('inf')], 'mets': 4.9})});
export var ICEV_WH_PER_KM = 898.77;
export var HEV_WH_PER_KM = 625.22;
export var PHEV_ELEC_WH_PER_KM = 289.1;
export var PHEV_GAS_WH_PER_KM = 663.5;
export var BEV_WH_PER_KM = 286.8;
export var RIDEHAIL_WH_PER_KM = 1198.36;
export var AIR_WH_PER_KM = 493.91;
export var E_BIKE_WH_PER_KM = 13.67;
export var BIKESHARE_WH_PER_TRIP = 90;
export var SCOOTERSHARE_WH_PER_KM = 16.78;
export var SCOOTERSHARE_WH_PER_TRIP = 4.1;
export var MOPED_WH_PER_KM = mpge_to_wh_per_km (100);
export var PHEV_UF = 0.37;
export var AIR_FOOTPRINT = dict ({'jet_fuel': dict ({'wh_per_km': AIR_WH_PER_KM})});
export var CAR_FOOTPRINT = dict ({'gasoline': dict ({'wh_per_km': ICEV_WH_PER_KM})});
export var E_CAR_FOOTPRINT = dict ({'electric': dict ({'wh_per_km': BEV_WH_PER_KM})});
export var PHEV_CAR_FOOTPRINT = dict ({'electric': dict ({'wh_per_km': PHEV_ELEC_WH_PER_KM, 'weight': PHEV_UF}), 'gasoline': dict ({'wh_per_km': PHEV_GAS_WH_PER_KM, 'weight': 1 - PHEV_UF})});
export var E_BIKE_FOOTPRINT = dict ({'electric': dict ({'wh_per_km': E_BIKE_WH_PER_KM})});
export var E_SCOOTER_FOOTPRINT = dict ({'electric': dict ({'wh_per_km': SCOOTERSHARE_WH_PER_KM, 'wh_per_trip': SCOOTERSHARE_WH_PER_TRIP})});
export var BIKESHARE_FOOTPRINT = dict ({'diesel': dict ({'wh_per_trip': BIKESHARE_WH_PER_TRIP})});
export var MOPED_FOOTPRINT = dict ({'gasoline': dict ({'wh_per_km': MOPED_WH_PER_KM})});
export var TAXI_FOOTPRINT = dict ({'gasoline': dict ({'wh_per_km': RIDEHAIL_WH_PER_KM})});
export var BASE_MODES = dict ({'IN_VEHICLE': dict ({'icon': 'speedometer', 'color': mode_colors ['red'], 'met': dict ({})}), 'BICYCLING': dict ({'icon': 'bike', 'color': mode_colors ['green'], 'met': BIKING_METS, 'footprint': dict ({})}), 'ON_FOOT': dict ({'icon': 'walk', 'color': mode_colors ['blue'], 'met': WALKING_METS, 'footprint': dict ({})}), 'UNKNOWN': dict ({'icon': 'help', 'color': mode_colors ['grey']}), 'WALKING': dict ({'icon': 'walk', 'color': mode_colors ['blue'], 'met': WALKING_METS, 'footprint': dict ({})}), 'AIR_OR_HSR': dict ({'icon': 'airplane', 'color': mode_colors ['orange'], 'met': dict ({}), 'footprint': AIR_FOOTPRINT}), 'CAR': dict ({'icon': 'car', 'color': mode_colors ['red'], 'met': dict ({}), 'footprint': CAR_FOOTPRINT}), 'E_CAR': dict ({'icon': 'car-electric', 'color': mode_colors ['pink'], 'met': dict ({}), 'footprint': E_CAR_FOOTPRINT}), 'PHEV_CAR': dict ({'icon': 'car-electric', 'color': mode_colors ['pink'], 'met': dict ({}), 'footprint': PHEV_CAR_FOOTPRINT}), 'E_BIKE': dict ({'icon': 'bicycle-electric', 'color': mode_colors ['green'], 'met': E_BIKING_METS, 'footprint': E_BIKE_FOOTPRINT}), 'E_SCOOTER': dict ({'icon': 'scooter-electric', 'color': mode_colors ['periwinkle'], 'met': dict ({}), 'footprint': E_SCOOTER_FOOTPRINT}), 'BIKESHARE': dict ({'icon': 'bicycle', 'color': mode_colors ['green'], 'met': BIKING_METS, 'footprint': BIKESHARE_FOOTPRINT}), 'MOPED': dict ({'icon': 'moped', 'color': mode_colors ['green'], 'met': dict ({}), 'footprint': MOPED_FOOTPRINT}), 'TAXI': dict ({'icon': 'taxi', 'color': mode_colors ['red'], 'met': dict ({}), 'footprint': TAXI_FOOTPRINT}), 'BUS': dict ({'icon': 'bus-side', 'color': mode_colors ['magenta'], 'met': dict ({}), 'footprint': dict ({'transit': ['MB', 'RB', 'CB']})}), 'AIR': dict ({'icon': 'airplane', 'color': mode_colors ['orange'], 'met': dict ({}), 'footprint': AIR_FOOTPRINT}), 'LIGHT_RAIL': dict ({'icon': 'train-car-passenger', 'color': mode_colors ['periwinkle'], 'met': dict ({}), 'footprint': dict ({'transit': ['LR']})}), 'TRAIN': dict ({'icon': 'train-car-passenger', 'color': mode_colors ['periwinkle'], 'met': dict ({}), 'footprint': dict ({'transit': ['LR', 'HR', 'YR', 'CR']})}), 'TRAM': dict ({'icon': 'tram', 'color': mode_colors ['periwinkle'], 'met': dict ({}), 'footprint': dict ({'transit': ['SR']})}), 'SUBWAY': dict ({'icon': 'subway-variant', 'color': mode_colors ['periwinkle'], 'met': dict ({}), 'footprint': dict ({'transit': ['HR']})}), 'FERRY': dict ({'icon': 'ferry', 'color': mode_colors ['taupe'], 'met': dict ({}), 'footprint': dict ({'transit': ['FB']})}), 'TROLLEYBUS': dict ({'icon': 'bus-side', 'color': mode_colors ['taupe'], 'met': dict ({}), 'footprint': dict ({'transit': ['TB', 'SR']})}), 'UNPROCESSED': dict ({'icon': 'help', 'color': mode_colors ['grey']}), 'OTHER': dict ({'icon': 'pencil-circle', 'color': mode_colors ['taupe']}), 'NONE': dict ({'icon': 'cancel', 'color': mode_colors ['grey'], 'met': dict ({}), 'footprint': dict ({})})});
export var get_base_mode_by_key = function (motionName) {
	var key = ('' + motionName).upper ();
	var py_pop = key.py_split ('.').py_pop ();
	return BASE_MODES.py_get (py_pop, BASE_MODES ['UNKNOWN']);
};
export var get_rich_mode_for_value = function (value, label_options) {
	if (!__in__ ('MODE', label_options)) {
		Log.error ('No MODE in label_options');
		return null;
	}
	for (var opt of label_options ['MODE']) {
		if (__in__ ('value', opt) && opt ['value'] == value) {
			return get_rich_mode (opt);
		}
	}
	return get_base_mode_by_key (value);
};
export var get_rich_mode = function (label_option) {
	var rich_mode = (function () {
		var __accu0__ = [];
		for (var [k, v] of dict (label_option).py_items ()) {
			__accu0__.append ([k, v]);
		}
		return dict (__accu0__);
	}) ();
	var base_props = ['icon', 'color', 'met', 'footprint'];
	for (var prop of base_props) {
		if (__in__ (prop, label_option)) {
			rich_mode [prop] = label_option [prop];
		}
		else if (__in__ ('{}_equivalent'.format (prop), label_option)) {
			var eq_base_mode = get_base_mode_by_key (label_option ['{}_equivalent'.format (prop)]);
			if (__in__ (prop, eq_base_mode)) {
				rich_mode [prop] = eq_base_mode [prop];
			}
			else {
				Log.warn ('Opt {} had {}_equivalent={} but {} not in {}'.format (label_option ['value'], prop, label_option ['{}_equivalent'.format (prop)], prop, eq_base_mode));
			}
		}
		else {
			for (var bm of ['base_mode', 'baseMode']) {
				if (__in__ (bm, label_option)) {
					var base_mode = get_base_mode_by_key (label_option [bm]);
					if (__in__ (prop, base_mode)) {
						rich_mode [prop] = base_mode [prop];
					}
				}
			}
		}
	}
	return rich_mode;
};
export var scale_lightness = function (hex_color, factor) {
	if (!(hex_color)) {
		return hex_color;
	}
	var color_obj = color (hex_color);
	if (factor < 1) {
		return color_obj.darken (1 - factor).hex ();
	}
	else {
		return color_obj.lighten (factor - 1).hex ();
	}
};
export var dedupe_colors = function (colors, adjustment_range) {
	if (typeof adjustment_range == 'undefined' || (adjustment_range != null && adjustment_range.hasOwnProperty ("__kwargtrans__"))) {;
		adjustment_range = [1, 2];
	};
	var colors_deduped = dict ({});
	for (var [key, color] of colors) {
		if (!(color) || __in__ (key, colors_deduped)) {
			continue;
		}
		var duplicates = (function () {
			var __accu0__ = [];
			for (var color_pair of colors) {
				if (color_pair [1] == color) {
					__accu0__.append (color_pair);
				}
			}
			return __accu0__;
		}) ();
		if (len (duplicates) > 1) {
			for (var [i, [k, c]] of enumerate (duplicates)) {
				var __left0__ = adjustment_range;
				var min_adj = __left0__ [0];
				var max_adj = __left0__ [1];
				var factor = min_adj + ((max_adj - min_adj) / (len (duplicates) - 1)) * i;
				colors_deduped [k] = scale_lightness (c, factor);
			}
		}
		else {
			colors_deduped [key] = color;
		}
	}
	return colors_deduped;
};

//# sourceMappingURL=emcommon.diary.base_modes.map