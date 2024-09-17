// Transcrypt'ed from Python, 2024-09-17 17:17:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as emcmfu from './emcommon.metrics.footprint.util.js';
import * as Log from './emcommon.logger.js';
export {emcmfu, Log};
var __name__ = 'emcommon.metrics.footprint.egrid';
export var get_egrid_intensity = async function (year, coords, region, metadata) {
	if (typeof coords == 'undefined' || (coords != null && coords.hasOwnProperty ("__kwargtrans__"))) {;
		coords = null;
	};
	if (typeof region == 'undefined' || (region != null && region.hasOwnProperty ("__kwargtrans__"))) {;
		region = null;
	};
	if (typeof metadata == 'undefined' || (metadata != null && metadata.hasOwnProperty ("__kwargtrans__"))) {;
		metadata = dict ({});
	};
	if (region === null) {
		metadata.py_update (dict ({'requested_coords': coords}));
		region = await emcmfu.get_egrid_region (coords, year);
	}
	return await get_egrid_intensity_for_region (year, region, metadata);
};
export var get_egrid_intensity_for_region = async function (year, region, metadata) {
	if (typeof metadata == 'undefined' || (metadata != null && metadata.hasOwnProperty ("__kwargtrans__"))) {;
		metadata = dict ({});
	};
	var intensities_data = await emcmfu.get_intensities_data (year, 'egrid');
	var actual_year = intensities_data ['metadata'] ['year'];
	metadata.py_update (dict ({'data_sources': ['egrid{}'.format (actual_year)], 'data_source_urls': intensities_data ['metadata'] ['data_source_urls'], 'is_provisional': actual_year != year, 'requested_year': year, 'egrid_region': region}));
	if (region !== null && __in__ (region, intensities_data ['regions_kg_per_mwh'])) {
		var kg_per_kwh = intensities_data ['regions_kg_per_mwh'] [region];
	}
	else {
		Log.warn ('eGRID region not found for region {} in year {}. Using national average.'.format (region, year));
		var kg_per_kwh = intensities_data ['national_kg_per_mwh'];
	}
	return tuple ([kg_per_kwh, metadata]);
};

//# sourceMappingURL=emcommon.metrics.footprint.egrid.map