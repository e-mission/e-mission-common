// Transcrypt'ed from Python, 2024-08-27 12:55:27
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as base_modes from './emcommon.diary.base_modes.js';
import * as footprint_calculations from './emcommon.metrics.footprint.footprint_calculations.js';
import * as ble_matching from './emcommon.bluetooth.ble_matching.js';
import * as conditional_surveys from './emcommon.survey.conditional_surveys.js';
import * as active_travel_calculations from './emcommon.metrics.active_travel.active_travel_calculations.js';
import * as metrics_summaries from './emcommon.metrics.metrics_summaries.js';
import * as Log from './emcommon.logger.js';
export {conditional_surveys, base_modes, active_travel_calculations, metrics_summaries, footprint_calculations, Log, ble_matching};
var __name__ = '__main__';
export var dict_to_js_obj = function (py_dict) {
	var js_obj = {};
	for (var [key, value] of py_dict.py_items ()) {
		if (isinstance (value, dict)) {
			js_obj [key] = dict_to_js_obj (value);
		}
		else {
			js_obj [key] = value;
		}
	}
	return js_obj;
};

//# sourceMappingURL=index.map