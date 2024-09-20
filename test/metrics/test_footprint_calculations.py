
import emcommon.metrics.footprint.footprint_calculations as emcmff
import emcommon.metrics.footprint.util as emcmfu
from ..__testing import jest_test, jest_describe, expectEqual, expectAlmostEqual


@jest_test
async def test_car_footprint():
    """
    Test kWh and kg CO2e for a 1 km trip in the default CAR.
    """
    fake_trip = {
        "_id": 'fake_trip_id',
        "distance": 1000,
        "start_fmt_time": "0000-00-00T00:00:00",
        "start_loc": {"coordinates": [0, 0]},
        "user_input": {"mode_confirm": "default_car"}
    }
    fake_label_options = {
        "MODE": [
            {"value": "default_car", "base_mode": "CAR"}
        ]
    }

    (footprint, metadata) = await emcmff.calc_footprint_for_trip(fake_trip, fake_label_options)

    expected_footprint = {'kwh': 0.899, 'kg_co2': 0.291}
    for key in expected_footprint.keys():
        expectAlmostEqual(footprint[key], expected_footprint[key], delta=0.001)

    # with 2 passengers, the footprint should be halved
    fake_label_options['MODE'][0]['passengers'] = 2

    (footprint, metadata) = await emcmff.calc_footprint_for_trip(fake_trip, fake_label_options)

    expected_footprint = {'kwh': 0.899 / 2, 'kg_co2': 0.291 / 2}
    for key in expected_footprint.keys():
        expectAlmostEqual(footprint[key], expected_footprint[key], delta=0.001)


@jest_test
async def test_ebike_footprint():
    """
    Test kWh and kg CO2e for a 1 km trip in the default E_BIKE.
    """
    fake_trip = {
        "_id": "fake_trip_id",
        "distance": 1000,
        "start_fmt_time": "0000-00-00T00:00:00",
        "start_loc": {"coordinates": [0, 0]},
        "user_input": {"mode_confirm": "ebike"}
    }
    fake_label_options = {
        "MODE": [
            {"value": "ebike", "base_mode": "E_BIKE"}
        ]
    }

    (footprint, metadata) = await emcmff.calc_footprint_for_trip(fake_trip, fake_label_options)

    expected_footprint = {'kwh': 0.014, 'kg_co2': 0.006}
    for key in expected_footprint.keys():
        expectAlmostEqual(footprint[key], expected_footprint[key], delta=0.001)


@jest_test
async def test_custom_car_footprint():
    """
    Test kWh and kg CO2e for a 10 km trip in a custom CAR (wh/km = 100).
    """
    fake_trip = {
        "_id": "fake_trip_id",
        "distance": 1000,
        "start_fmt_time": "0000-00-00T00:00:00",
        "start_loc": {"coordinates": [0, 0]},
        "user_input": {"mode_confirm": "custom_car"}
    }
    fake_label_options = {
        "MODE": [
            {"value": "custom_car", "passengers": 1, "footprint": {"gasoline": {"wh_per_km": 100}}}
        ]
    }

    (footprint, metadata) = await emcmff.calc_footprint_for_trip(fake_trip, fake_label_options)

    expected_footprint = {
        'kwh': 0.1,
        'kg_co2': (0.1 / 1000) * emcmfu.FUELS_KG_CO2_PER_MWH['gasoline']
    }
    for key in expected_footprint.keys():
        expectAlmostEqual(footprint[key], expected_footprint[key], delta=0.01)


@jest_test
async def test_nyc_bus_footprint():
    """
    Test kWh and kg CO2e for a 10 km bus trip in NYC.
    """
    fake_trip = {
        "_id": "fake_trip_id",
        "distance": 10000,
        "start_fmt_time": "2022-01-01",
        "start_loc": {"coordinates": [-74.006, 40.7128]},
        "user_input": {"mode_confirm": "bus"},
    }
    fake_label_options = {
        "MODE": [
            {"value": "bus", "base_mode": "BUS"}
        ]
    }

    (footprint, metadata) = await emcmff.calc_footprint_for_trip(fake_trip, fake_label_options)

    expected_footprint = {'kwh': 12.93, 'kg_co2': 2.80}
    expected_metadata = {
        "data_sources": ["ntd2022", "egrid2022"],
        "is_provisional": False,
        "requested_year": 2022,
        "ntd_uace_code": "63217",
        "ntd_modes": ["MB", "RB", "CB"],
    }
    for key in expected_footprint.keys():
        expectAlmostEqual(footprint[key], expected_footprint[key], delta=0.01)
    for key in expected_metadata.keys():
        expectEqual(metadata[key], expected_metadata[key])


@jest_test
async def test_impact_of_ebike_replacing_car():
    """
    Test kWh and kg CO2e saved for a 1 km trip where E_BIKE replaced CAR.
    """
    fake_trip = {
        "_id": "fake_trip_id",
        "distance": 1000,
        "start_fmt_time": "0000-00-00T00:00:00",
        "start_loc": {"coordinates": [0, 0]},
        "user_input": {"mode_confirm": "ebike", "replaced_mode_confirm": "car"}
    }
    fake_label_options = {
        "MODE": [
            {"value": "car", "base_mode": "CAR"},
            {"value": "ebike", "base_mode": "E_BIKE"}
        ]
    }

    (mode_footprint, metadata) = await emcmff.calc_footprint_for_trip(
        fake_trip,
        fake_label_options
    )
    (replaced_mode_footprint, metadata) = await emcmff.calc_footprint_for_trip(
        fake_trip,
        fake_label_options,
        'replaced_mode'
    )
    kwh_saved = replaced_mode_footprint['kwh'] - mode_footprint['kwh']
    kg_co2_saved = replaced_mode_footprint['kg_co2'] - mode_footprint['kg_co2']

    expectAlmostEqual(kwh_saved, 0.885, delta=0.001)
    expectAlmostEqual(kg_co2_saved, 0.285, delta=0.001)


jest_describe("test_footprint_calculations")
