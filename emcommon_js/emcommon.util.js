// Transcrypt'ed from Python, 2024-09-16 11:51:19
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'emcommon.util';
export var memoize = function (fn) {
	var _cache = dict ({});
	var wrapper = function () {
		var kwargs = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete kwargs.__kwargtrans__;
			}
			var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
		}
		else {
			var args = tuple ();
		}
		if (!__in__ (tuple ([str (args), str (kwargs)]), _cache)) {
			_cache.__setitem__ ([str (args), str (kwargs)], fn (...args, __kwargtrans__ (kwargs)));
		}
		return _cache.__getitem__ ([str (args), str (kwargs)]);
	};
	return wrapper;
};
export var flatten_db_entry = function (entry) {
	
	      return {
	          ...entry.data,
	          _id: entry._id,
	          'user_id': entry.user_id,
	          key: entry.metadata.key,
	          origin_key: entry.metadata.origin_key
	      }
	    
};
export var resources = dict ({});
export var read_json_resource = async function (filename) {
	if (__in__ (filename, resources)) {
		return resources [filename];
	}
	
	    const r = await import("../src/emcommon/resources/" + filename);
	    resources[filename] = r.default;
	    return resources[filename];
	    
};
export var fetch_url = async function (url) {
	var response = await fetch (url);
	if (!(response.ok)) {
		var __except0__ = Exception ('Failed to fetch {}: {}'.format (url, response.text ()));
		__except0__.__cause__ = null;
		throw __except0__;
	}
	return await response.json ();
};

//# sourceMappingURL=emcommon.util.map