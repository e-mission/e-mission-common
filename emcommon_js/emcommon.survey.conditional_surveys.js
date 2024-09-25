// Transcrypt'ed from Python, 2024-09-25 01:43:16
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as Log from './emcommon.logger.js';
export {Log};
var __name__ = 'emcommon.survey.conditional_surveys';
export var point_is_within_bounds = function (pt, bounds) {
	var lon_in_range = pt [0] > bounds [0] [0] && pt [0] < bounds [1] [0];
	var lat_in_range = pt [1] < bounds [0] [1] && pt [1] > bounds [1] [1];
	return lat_in_range && lon_in_range;
};
export var conditional_survey_fns = dict ({'pointIsWithinBounds': point_is_within_bounds});
export var scoped_eval = function (script, scope) {
	
	        return Function(...Object.keys(scope), `return ${script}`)(...Object.values(scope));
	    
};
export var get_shows_if_condition = function (survey) {
	return survey ['showsIf'];
};
export var survey_prompted_for_trip = function (composite_trip, app_config) {
	var potential_surveys = null;
	try {
		var potential_surveys = app_config ['survey_info'] ['buttons'] ['trip-label'];
	}
	catch (__except0__) {
		Log.warn ('No surveys in app config');
		return null;
	}
	if (!(isinstance (potential_surveys, list))) {
		return potential_surveys ['surveyName'];
	}
	for (var survey of potential_surveys) {
		var shows_if = get_shows_if_condition (survey);
		var scope = dict (composite_trip);
		scope.py_update (conditional_survey_fns);
		var shows_if = shows_if.py_replace ('confirmedMode?.baseMode', 'primary_ble_sensed_mode');
		if (!__in__ ('primary_ble_sensed_mode', scope)) {
			try {
				scope ['primary_ble_sensed_mode'] = scope ['confirmedMode'] ['baseMode'];
			}
			catch (__except0__) {
				scope ['primary_ble_sensed_mode'] = null;
			}
		}
		try {
			if (scoped_eval (shows_if, scope)) {
				return survey ['surveyName'];
			}
		}
		catch (__except0__) {
			if (isinstance (__except0__, Exception)) {
				var e = __except0__;
				Log.error ('Error evaluating showsIf for survey {}: {}'.format (survey, e));
			}
			else Log.error ('Error evaluating showsIf for survey {}: {}'.format (survey, __except0__));
		}
	}
	return null;
};

//# sourceMappingURL=emcommon.survey.conditional_surveys.map