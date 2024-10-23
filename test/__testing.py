def _expect(condition):
    assert condition  # __: skip
    '''?
    expect(condition).toBeTruthy()
    ?'''


def expectEqual(a, b):
    assert a == b  # __: skip
    '''?
    expect(a).toEqual(b)
    ?'''


# __pragma__('kwargs')
def expectAlmostEqual(a, b, places=3):
    assert abs(a - b) < (.5 / 10 ** places)  # __: skip
    '''?
    expect(a).toBeCloseTo(b, places)
    ?'''
# __pragma__('nokwargs')


def jest_test(test):
    '''?
    window['jest_tests'] = window['jest_tests'] or []
    window['jest_tests'].append(test)
    ?'''
    return test


def jest_describe(describe_name):
    '''?
    tests = window['jest_tests'] or []
    expect(tests.length).toBeGreaterThan(0)
    def run_tests():
        for t in tests:
            test(t.js_name, t)

    describe(describe_name, run_tests);
    ?'''
    pass
