export function __nest__(headObject: any, tailNames: any, value: any): void;
export function __init__(module: any): any;
export function __get__(aThis: any, func: any, quotedFuncName: any): any;
export function __getcm__(aThis: any, func: any, quotedFuncName: any): (...args: any[]) => any;
export function __getsm__(aThis: any, func: any, quotedFuncName: any): any;
export function __class__(name: any, bases: any, attribs: any, meta: any): any;
export function __pragma__(): void;
export function __call__(...args: any[]): any;
export function __kwargtrans__(anObject: any): any;
export function __super__(aClass: any, methodName: any): any;
export function property(getter: any, setter: any): {
    get: () => any;
    set: (value: any) => void;
    enumerable: boolean;
};
export function __setproperty__(anObject: any, name: any, descriptor: any): void;
export function assert(condition: any, message: any): void;
export function __mergekwargtrans__(object0: any, object1: any): {};
export function __mergefields__(targetClass: any, sourceClass: any): void;
export function __withblock__(manager: any, statements: any): void;
export function dir(obj: any): string[];
export function setattr(obj: any, name: any, value: any): void;
export function getattr(obj: any, name: any): any;
export function hasattr(obj: any, name: any): boolean;
export function delattr(obj: any, name: any): void;
export function __in__(element: any, container: any): any;
export function __specialattrib__(attrib: any): any;
export function len(anObject: any): any;
export function __i__(any: any): any;
export function __k__(keyed: any, key: any): any;
export function __t__(target: any): any;
export function float(any: any): number;
export namespace float {
    let __name__: string;
    let __bases__: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
}
export function int(any: any): number;
export namespace int {
    let __name___1: string;
    export { __name___1 as __name__ };
    let __bases___1: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
    export { __bases___1 as __bases__ };
}
export function bool(any: any): boolean;
export namespace bool {
    let __name___2: string;
    export { __name___2 as __name__ };
    let __bases___2: (typeof int)[];
    export { __bases___2 as __bases__ };
}
export function py_typeof(anObject: any): any;
export function issubclass(aClass: any, classinfo: any): boolean;
export function isinstance(anObject: any, classinfo: any): boolean;
export function callable(anObject: any): boolean;
export function repr(anObject: any): any;
export function chr(charCode: any): string;
export function ord(aChar: any): any;
export function max(...args: any[]): any;
export function min(...args: any[]): any;
export function bin(nbr: any): string;
export function oct(nbr: any): string;
export function hex(nbr: any): string;
export function round(number: any, ndigits: any): number;
export function __jsUsePyNext__(): {
    value: any;
    done: boolean;
};
export function __pyUseJsNext__(): any;
export function py_iter(iterable: any): any;
export function py_next(iterator: any): any;
export function __PyIterator__(iterable: any): void;
export class __PyIterator__ {
    constructor(iterable: any);
    iterable: any;
    index: number;
    __next__(): any;
}
export function __JsIterator__(iterable: any): void;
export class __JsIterator__ {
    constructor(iterable: any);
    iterable: any;
    index: number;
    next(): {
        value: number;
        done: boolean;
    };
}
export function py_reversed(iterable: any): any;
export function zip(...args: any[]): any;
export function range(start: any, stop: any, step: any): any[];
export function any(iterable: any): boolean;
export function all(iterable: any): boolean;
export function sum(iterable: any): number;
export function enumerate(iterable: any, start?: number): any;
export function list(iterable: any): any[];
export namespace list {
    let __name___3: string;
    export { __name___3 as __name__ };
    let __bases___3: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
    export { __bases___3 as __bases__ };
}
export function tuple(iterable: any): any;
export namespace tuple {
    let __name___4: string;
    export { __name___4 as __name__ };
    let __bases___4: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
    export { __bases___4 as __bases__ };
}
export function set(iterable: any): any[];
export namespace set {
    let __name___5: string;
    export { __name___5 as __name__ };
    let __bases___5: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
    export { __bases___5 as __bases__ };
}
export function bytearray(bytable: any, encoding: any): Uint8Array<any>;
export function str(stringable: any): any;
export namespace str {
    let __name___6: string;
    export { __name___6 as __name__ };
    let __bases___6: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
    export { __bases___6 as __bases__ };
}
export function dict(objectOrPairs: any): {};
export namespace dict {
    let __name___7: string;
    export { __name___7 as __name__ };
    let __bases___7: {
        __init__: (self: any) => void;
        __metaclass__: {
            __name__: string;
            __bases__: any[];
            __new__: (meta: any, name: any, bases: any, attribs: any) => {
                (...args: any[]): any;
                __metaclass__: any;
                __name__: any;
                __bases__: any;
            };
        };
        __name__: string;
        __bases__: any[];
        __new__: (args: any) => any;
    }[];
    export { __bases___7 as __bases__ };
}
export function __jsmod__(a: any, b: any): any;
export function __mod__(a: any, b: any): any;
export function __pow__(a: any, b: any): any;
export function __neg__(a: any): any;
export function __matmul__(a: any, b: any): any;
export function __mul__(a: any, b: any): any;
export function __truediv__(a: any, b: any): any;
export function __floordiv__(a: any, b: any): any;
export function __add__(a: any, b: any): any;
export function __sub__(a: any, b: any): any;
export function __lshift__(a: any, b: any): any;
export function __rshift__(a: any, b: any): any;
export function __or__(a: any, b: any): any;
export function __xor__(a: any, b: any): any;
export function __and__(a: any, b: any): any;
export function __eq__(a: any, b: any): any;
export function __ne__(a: any, b: any): any;
export function __lt__(a: any, b: any): any;
export function __le__(a: any, b: any): any;
export function __gt__(a: any, b: any): any;
export function __ge__(a: any, b: any): any;
export function __imatmul__(a: any, b: any): any;
export function __ipow__(a: any, b: any): any;
export function __ijsmod__(a: any, b: any): any;
export function __imod__(a: any, b: any): any;
export function __imul__(a: any, b: any): any;
export function __idiv__(a: any, b: any): any;
export function __iadd__(a: any, b: any): any;
export function __isub__(a: any, b: any): any;
export function __ilshift__(a: any, b: any): any;
export function __irshift__(a: any, b: any): any;
export function __ior__(a: any, b: any): any;
export function __ixor__(a: any, b: any): any;
export function __iand__(a: any, b: any): any;
export function __getitem__(container: any, key: any): any;
export function __setitem__(container: any, key: any, value: any): void;
export function __getslice__(container: any, lower: any, upper: any, step: any): any;
export function __setslice__(container: any, lower: any, upper: any, step: any, value: any): void;
export { _copy };
export namespace __envir__ {
    export let interpreter_name: string;
    export let transpiler_name: string;
    import executor_name = transpiler_name;
    export { executor_name };
    export let transpiler_version: string;
}
export namespace py_metatype {
    export { py_metatype as __metaclass__ };
}
export namespace object {
    export function __init__(self: any): void;
    export { py_metatype as __metaclass__ };
    let __name___8: string;
    export { __name___8 as __name__ };
    let __bases___8: any[];
    export { __bases___8 as __bases__ };
    export function __new__(args: any): any;
}
export const abs: (x: number) => number;
export function bytes(bytable: any, encoding: any): Uint8Array<any>;
export function pow(a: any, b: any): any;
export const BaseException: any;
export const Exception: any;
export const IterableError: any;
export const StopIteration: any;
export const ValueError: any;
export const KeyError: any;
export const AssertionError: any;
export const NotImplementedError: any;
export const IndexError: any;
export const AttributeError: any;
export const py_TypeError: any;
export const Warning: any;
export const UserWarning: any;
export const DeprecationWarning: any;
export const RuntimeWarning: any;
export function _sort(iterable: any, key: any, reverse: any, ...args: any[]): void;
export function sorted(iterable: any, ...args: any[]): any;
export function __sort__(iterable: any, ...args: any[]): void;
export function map(func: any, ...args: any[]): any[];
export function filter(func: any, iterable: any): any[];
export function divmod(n: any, d: any): any;
export const __Terminal__: any;
export const __terminal__: any;
export const print: any;
export const input: any;
import { copy as _copy } from './copy.js';
//# sourceMappingURL=org.transcrypt.__runtime__.d.ts.map