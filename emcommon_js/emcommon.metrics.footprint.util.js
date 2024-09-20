// Transcrypt'ed from Python, 2024-09-17 17:17:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {fetch_url, read_json_resource} from './emcommon.util.js';
import * as Log from './emcommon.logger.js';
export {fetch_url, read_json_resource, Log};
var __name__ = 'emcommon.metrics.footprint.util';
export var MI_PER_KM = 0.621371;
export var KWH_PER_GGE = 33.41;
export var MPGE_KWH_PER_GAL = 33.7;
export var KWH_PER_GAL_GASOLINE = KWH_PER_GGE * 1.0;
export var KWH_PER_GAL_DIESEL = KWH_PER_GGE * 1.14;
export var KWH_PER_GAL_BIODIESEL = KWH_PER_GGE * 1.05;
export var KWH_PER_GAL_LPG = KWH_PER_GGE * 0.74;
export var KWH_PER_GAL_CNG = KWH_PER_GGE * 0.26;
export var KWH_PER_KG_HYDROGEN = KWH_PER_GGE * 1.0;
export var KWH_PER_GAL_OTHER = KWH_PER_GGE * 1.0;
export var FUELS_KG_CO2_PER_MWH = dict ({'gasoline': 324.183, 'diesel': 325.073, 'jet_fuel': 304.354, 'lpg': 279.192, 'cng': 271.024, 'hydrogen': 332.852});
export var mpge_to_wh_per_km = function (mpge) {
	return ((MI_PER_KM / mpge) * MPGE_KWH_PER_GAL) * 1000;
};
export var year_of_trip = function (trip) {
	return int (trip ['start_fmt_time'].py_split ('-') [0]);
};
export var is_point_inside_polygon = function (pt, vs) {
	var __left0__ = pt;
	var x = __left0__ [0];
	var y = __left0__ [1];
	var inside = false;
	var j = len (vs) - 1;
	for (var i = 0; i < len (vs); i++) {
		var __left0__ = vs [i];
		var xi = __left0__ [0];
		var yi = __left0__ [1];
		var __left0__ = vs [j];
		var xj = __left0__ [0];
		var yj = __left0__ [1];
		var intersect = yi > y != yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
		if (intersect) {
			var inside = !(inside);
		}
		var j = i;
	}
	return inside;
};
export var get_feature_containing_point = function (pt, geojson) {
	for (var feature of geojson ['features']) {
		if (feature ['geometry'] ['type'] == 'Polygon') {
			var polys = [feature ['geometry'] ['coordinates']];
		}
		else if (feature ['geometry'] ['type'] == 'MultiPolygon') {
			var polys = feature ['geometry'] ['coordinates'];
		}
		for (var poly of polys) {
			if (is_point_inside_polygon (pt, poly [0])) {
				return feature;
			}
		}
	}
	return null;
};
export var latest_egrid_year = null;
export var latest_ntd_year = null;
export var get_egrid_region = async function (coords, year) {
	if (year < 2018) {
		Log.warn ('eGRID data not available for {}. Using 2018.'.format (year));
		return await get_egrid_region (coords, 2018);
	}
	if (latest_egrid_year !== null && year > latest_egrid_year) {
		return await get_egrid_region (coords, latest_egrid_year);
	}
	try {
		var geojson = await read_json_resource ('egrid{}_subregions_5pct.json'.format (year));
	}
	catch (__except0__) {
		if (year > 2018) {
			Log.warn ('eGRID data not available for {}. Trying {}.'.format (year, year - 1));
			latest_egrid_year = year - 1;
			return await get_egrid_region (coords, year - 1);
		}
		Log.error ('eGRID lookup failed for {}.'.format (year));
		return null;
	}
	var region_feature = get_feature_containing_point (coords, geojson);
	if (region_feature !== null) {
		return region_feature ['properties'] ['name'];
	}
	Log.warn ('An eGRID region was not found for coords {} in year {}.'.format (coords, year));
	return null;
};
export var get_uace_by_coords = async function (coords, year) {
    var census_year = year - __mod__ (year, 10);
    var url = ('https://geocoding.geo.census.gov/geocoder/geographies/coordinates?' + 'x={}&y={}'.format (coords [0], coords [1])) + '&benchmark=Public_AR_Current&vintage=Census{}_Current&layers=87&format=json'.format (census_year);
    try {
        var data = await fetch_url (url);
    }
    catch (__except0__) {
        if (isinstance (__except0__, Exception)) {
            var e = __except0__;
            Log.error ('Failed to geocode {} in year {}: {}'.format (coords, year, e));
            console.error('Exception:', e);  // Print the exception
            return null;
        }
        else {
            Log.error ('Failed to geocode {} in year {}'.format (coords, year));
            console.error('Exception:', __except0__);  // Print the exception
            return null;
        }
    }
    for (var g in data ['result'] ['geographies']) {
        for (var entry of data ['result'] ['geographies'] [g]) {
            if (__in__ ('UA', entry)) {
                return entry ['UA'];
            }
        }
    }
    Log.warn ('Urban Area not in geocoding response for coords {} in year {}: {}'.format (coords, year, url));
    return null;
};
export var get_intensities_data = async function (year, dataset) {
	if (year < 2018) {
		Log.warn ('{} data not available for {}. Using 2018.'.format (dataset, year));
		return await get_intensities_data (2018, dataset);
	}
	if (dataset == 'egrid' && latest_egrid_year !== null && year > latest_egrid_year) {
		return await get_intensities_data (latest_egrid_year, dataset);
	}
	if (dataset == 'ntd' && latest_ntd_year !== null && year > latest_ntd_year) {
		return await get_intensities_data (latest_ntd_year, dataset);
	}
	try {
		return await read_json_resource ('{}{}_intensities.json'.format (dataset, year));
	}
	catch (__except0__) {
		if (year > 2018) {
			Log.warn ('{} data not available for {}. Trying {}.'.format (dataset, year, year - 1));
			if (dataset == 'egrid') {
				latest_egrid_year = year - 1;
			}
			else if (dataset == 'ntd') {
				latest_ntd_year = year - 1;
			}
			return await get_intensities_data (year - 1, dataset);
		}
		Log.error ('eGRID lookup failed for {}.'.format (year));
		return null;
	}
};
export var merge_metadatas = function (meta_a, meta_b) {
	for (var key in meta_b) {
		var value = meta_b [key];
		if (!__in__ (key, meta_a)) {
			meta_a [key] = value;
		}
		else if (hasattr (meta_a [key], 'concat')) {
			meta_a [key] = meta_a [key].concat ((function () {
				var __accu0__ = [];
				for (var v of value) {
					if (!__in__ (v, meta_a [key])) {
						__accu0__.append (v);
					}
				}
				return __accu0__;
			}) ());
		}
		else if (isinstance (value, list)) {
			meta_a [key] = meta_a [key] + (function () {
				var __accu0__ = [];
				for (var v of value) {
					if (!__in__ (v, meta_a [key])) {
						__accu0__.append (v);
					}
				}
				return __accu0__;
			}) ();
		}
		else if (isinstance (value, bool)) {
			meta_a [key] = meta_a [key] || value;
		}
		else {
			meta_a [key] = value;
		}
	}
};

//# sourceMappingURL=emcommon.metrics.footprint.util.map
