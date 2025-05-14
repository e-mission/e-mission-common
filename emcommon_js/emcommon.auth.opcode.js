// Transcrypt'ed from Python, 2025-05-13 19:52:13
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, _copy, _sort, abs, all, any, assert, bin, bool, bytearray, bytes, callable, chr, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, hex, input, int, isinstance, issubclass, len, list, map, max, min, object, oct, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = 'emcommon.auth.opcode';
export var ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
export var generate_random_string = function (length, charset) {
	if (typeof charset == 'undefined' || (charset != null && charset.hasOwnProperty ("__kwargtrans__"))) {;
		charset = null;
	};
	charset = charset || ALPHANUMERIC;
	var random_str = '';
	for (var _ = 0; _ < length; _++) {
		var random_index = Math.floor (Math.random () * charset.length);
		random_str += charset.charAt (random_index);
	}
	return random_str;
};
export var generate_opcode = function (prefix, program, subgroup, token_length) {
	var opcode_parts = [prefix, program];
	if (subgroup) {
		opcode_parts.append (subgroup);
	}
	opcode_parts.append (generate_random_string (token_length));
	return '_'.join (opcode_parts);
};

//# sourceMappingURL=emcommon.auth.opcode.map