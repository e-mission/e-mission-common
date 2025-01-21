from __future__ import annotations  # __: skip
import secrets  # __: skip


ALPHANUMERIC = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def generate_random_string(length: int, charset=None):
    '''
    Generates a random string of specified length in the specified charset
    :param length: the length of the string
    :param charset: the charset to use (optional, default is a-z, A-Z, 0-9)
    :return: a random string
    e.g. generate_random_string(12) -> 'BJnBJmt9JQcH'
         generate_random_string(20) -> '6qqTiyYxn2ExZAJRh53L
         generate_random_string(6, '0123456789') -> '503726'
    '''
    charset = charset or ALPHANUMERIC
    random_str = ''
    for _ in range(length):
        # JS implementation
        '''?
        random_index = Math.floor(Math.random() * charset.length);
        random_str += charset.charAt(random_index);
        ?'''
        # Python implementation
        random_str += secrets.choice(charset)  # __: skip
    return random_str


def generate_opcode(prefix: str, program: str, subgroup: str | None, token_length: int):
    opcode_parts = [prefix, program]
    if subgroup:
        opcode_parts.append(subgroup)
    opcode_parts.append(generate_random_string(token_length))
    return '_'.join(opcode_parts)
