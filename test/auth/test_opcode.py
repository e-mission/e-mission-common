import emcommon.auth.opcode as emcao
from ..__testing import _expect as expect, jest_test, jest_describe, expectEqual


@jest_test
def test_generate_random_string_alphanumeric():
    random_strs = [emcao.generate_random_string(12) for _ in range(100)]
    expectEqual(len(random_strs), 100)
    for random_string in random_strs:
        expectEqual(len(random_string), 12)
        expect(
            all(char in emcao.ALPHANUMERIC for char in random_string)
        )


@jest_test
def test_generate_random_string_vowels():
    VOWELS = 'AEIOUYaeiouy'
    random_strs = [emcao.generate_random_string(8, VOWELS) for _ in range(100)]
    expectEqual(len(random_strs), 100)
    for random_string in random_strs:
        expectEqual(len(random_string), 8)
        expect(
            all(char in VOWELS for char in random_string)
        )


@jest_test
def test_generate_opcode_with_subgroup():
    '''
    Generate and validate 100 opcodes for fake study 'hogwarts-transit'
    with subgroup 'gryffindor'
    '''
    opcodes = [
        emcao.generate_opcode('nrelop', 'hogwarts-transit', 'gryffindor', 10)
        for _ in range(100)
    ]
    expectEqual(len(opcodes), 100)
    for opcode in opcodes:
        opcode_parts = opcode.split('_')
        expect(len(opcode_parts) == 4)
        expect(opcode_parts[0] == 'nrelop')
        expect(opcode_parts[1] == 'hogwarts-transit')
        expect(opcode_parts[2] == 'gryffindor')
        expectEqual(len(opcode_parts[3]), 10)


@jest_test
def test_generate_opcode_without_subgroup():
    '''
    Generate and validate 100 opcodes for fake study 'coruscant-transit'
    with no subgroup
    '''
    opcodes = [
        emcao.generate_opcode('nrelop', 'coruscant-transit', None, 10)
        for _ in range(100)
    ]
    expectEqual(len(opcodes), 100)
    for opcode in opcodes:
        opcode_parts = opcode.split('_')
        expect(len(opcode_parts) == 3)
        expect(opcode_parts[0] == 'nrelop')
        expect(opcode_parts[1] == 'coruscant-transit')
        expectEqual(len(opcode_parts[2]), 10)


jest_describe('test_opcode')
