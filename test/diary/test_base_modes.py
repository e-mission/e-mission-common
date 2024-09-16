# __pragma__('jsiter')

import emcommon.diary.base_modes as emcdb
from ..__testing import _expect as expect, jest_test, jest_describe, expectEqual


@jest_test
def test_get_base_mode_by_key():
    base_mode = emcdb.get_base_mode_by_key("BUS")
    expected_base_mode = {
        "icon": 'bus-side',
        "color": emcdb.mode_colors['magenta'],
        "met": {},
        "footprint": {"transit": ["MB", "RB", "CB"]},
    }
    for key in expected_base_mode:
        expectEqual(str(base_mode[key]), str(expected_base_mode[key]))


@jest_test
def test_get_rich_mode_car():
    fake_label_option = {'base_mode': "CAR", 'passengers': 2}
    rich_mode = emcdb.get_rich_mode(fake_label_option)

    expected_rich_mode = {
        "base_mode": "CAR",
        "passengers": 2,
        "icon": 'car',
        "color": emcdb.mode_colors['red'],
        "met": {},
        "footprint": emcdb.CAR_FOOTPRINT,
    }
    for key in expected_rich_mode:
        expectEqual(str(rich_mode[key]), str(expected_rich_mode[key]))

    # ensure the original object was not mutated
    expectEqual(str(fake_label_option), str({'base_mode': "CAR", 'passengers': 2}))


@jest_test
def test_get_rich_mode_e_car():
    fake_label_option = {
        'baseMode': "E_CAR",  # with baseMode as camelCase, should still work
        'passengers': 1,
        'color': '#000000',
        'footprint': {'gasoline': {'wh_per_km': 500, 'weight': 1}}
    }
    rich_mode = emcdb.get_rich_mode(fake_label_option)

    expected_rich_mode = {
        "baseMode": "E_CAR",
        "passengers": 1,
        "color": '#000000',
        "footprint": {'gasoline': {'wh_per_km': 500, 'weight': 1}},
        "icon": 'car-electric',
        "met": {},
    }
    for key in expected_rich_mode:
        expectEqual(str(rich_mode[key]), str(expected_rich_mode[key]))

    # ensure the original object was not mutated
    expectEqual(str(fake_label_option),
                str({
                    'baseMode': "E_CAR",
                    'passengers': 1,
                    'color': '#000000',
                    'footprint': {'gasoline': {'wh_per_km': 500, 'weight': 1}}
                }))


fake_mode_colors = [
    ['walk', '#0074b7'],
    ['e-bike', '#008148'],
    ['bike', '#008148'],
    ['bikeshare', '#008148'],
]


@jest_test
def test_dedupe_colors():
    deduped_colors = emcdb.dedupe_colors(fake_mode_colors, [0.4, 1.6])

    expected = {
        'bike': '#008148',
        'bikeshare': '#00ce73',
        'e-bike': '#00341d',
        'walk': '#0074b7',
    }
    for mode in expected:
        expectEqual(deduped_colors[mode].upper(), expected[mode].upper())


@jest_test
def test_dedupe_colors_lighten_only():
    deduped_colors = emcdb.dedupe_colors(fake_mode_colors)

    expected = {
        'bike': '#00c26c',
        'bikeshare': '#03ff90',
        'e-bike': '#008148',
        'walk': '#0074b7',
    }
    for mode in expected:
        expectEqual(deduped_colors[mode].upper(), expected[mode].upper())


jest_describe('test_base_modes')

# __pragma__('nojsiter')
