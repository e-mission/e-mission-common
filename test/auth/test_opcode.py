import emcommon.auth.opcode as emcao
from ..__testing import _expect as expect, jest_test, jest_describe, expectEqual


@jest_test
def test_generate_random_string_alphanumeric():
    random_strs = [emcao.generate_random_string(10) for _ in range(100)]
    expectEqual(len(random_strs), 100)
    for random_string in random_strs:
        expectEqual(len(random_string), 10)
        expect(
            all(char in emcao.ALPHANUMERIC for char in random_string)
        )


@jest_test
def test_generate_random_string_vowels():
    VOWELS = 'AEIOUYaeiouy'
    random_strs = [emcao.generate_random_string(10, VOWELS) for _ in range(100)]
    expectEqual(len(random_strs), 100)
    for random_string in random_strs:
        expectEqual(len(random_string), 10)
        expect(
            all(char in VOWELS for char in random_string)
        )


jest_describe('test_opcode')
