import time
import emcommon.metrics.metrics_summaries as emcmms
from ..__testing import jest_test, jest_describe, expectEqual, expectAlmostEqual


def fake_trip(user_id, date, distance, mode, purpose):
    return {
        "_id": 'fake_trip_id',
        "user_id": user_id,
        "key": 'analysis/confirmed_trip',
        "distance": distance,
        "start_ts": date * 86400,
        "start_fmt_time": f'1970-01-0{date}T00:00:00',
        "start_loc": {"coordinates": [0, 0]},
        "user_input": {"mode_confirm": mode, "purpose_confirm": purpose}
    }


metric_list = {'distance': ['mode_confirm', 'purpose_confirm']}
fake_trips = [
    fake_trip('user_id_1', 1, 1000, 'e-car', 'home'),
    fake_trip('user_id_2', 1, 1000, 'e-car', 'meal'),
    fake_trip('user_id_1', 2, 2500, 'e-car', 'work'),
    fake_trip('user_id_2', 2, 500, 'bike', 'work'),
]


@jest_test
async def test_distance_metrics():
    summaries = await emcmms.generate_summaries(metric_list, fake_trips, {}, {})
    generated_time = time.time()

    day1_distance = next(d for d in summaries if d['date'] == '1970-01-01')
    expectEqual(day1_distance['metric'], 'distance')
    expectEqual(day1_distance['nUsers'], 2)
    expectAlmostEqual(day1_distance['last_updated'] / 1000, generated_time / 1000, places=1)
    day0_distance_mode_confirm = day1_distance['dimensions']['mode_confirm']
    e_car = next(d for d in day0_distance_mode_confirm if d['value'] == 'e-car')
    expectEqual(e_car['measure'], 2000)
    day0_distance_purpose_confirm = day1_distance['dimensions']['purpose_confirm']
    home = next(d for d in day0_distance_purpose_confirm if d['value'] == 'home')
    expectEqual(home['measure'], 1000)
    meal = next(d for d in day0_distance_purpose_confirm if d['value'] == 'meal')
    expectEqual(meal['measure'], 1000)

    day2_distance = next(d for d in summaries if d['date'] == '1970-01-02')
    expectEqual(day2_distance['metric'], 'distance')
    expectEqual(day2_distance['nUsers'], 2)
    expectAlmostEqual(day2_distance['last_updated'] / 1000, generated_time / 1000, places=1)
    day1_distance_mode_confirm = day2_distance['dimensions']['mode_confirm']
    e_car = next(d for d in day1_distance_mode_confirm if d['value'] == 'e-car')
    expectEqual(e_car['measure'], 2500)
    bike = next(d for d in day1_distance_mode_confirm if d['value'] == 'bike')
    expectEqual(bike['measure'], 500)
    day1_distance_purpose_confirm = day2_distance['dimensions']['purpose_confirm']
    work = next(d for d in day1_distance_purpose_confirm if d['value'] == 'work')
    expectEqual(work['measure'], 3000)


@jest_test
async def test_munged_distance_metrics():
    summaries = await emcmms.generate_summaries(metric_list, fake_trips, {}, {})
    munged_summaries = emcmms.munge_agg_metrics(summaries)

    day1_distance = next(d for d in munged_summaries['distance'] if d['date'] == '1970-01-01')
    expectEqual(day1_distance['nUsers'], 2)
    expectEqual(day1_distance['mode_confirm_e-car'], 2000)
    expectEqual(day1_distance['purpose_confirm_home'], 1000)
    expectEqual(day1_distance['purpose_confirm_meal'], 1000)

    day2_distance = next(d for d in munged_summaries['distance'] if d['date'] == '1970-01-02')
    expectEqual(day2_distance['nUsers'], 2)
    expectEqual(day2_distance['mode_confirm_e-car'], 2500)
    expectEqual(day2_distance['mode_confirm_bike'], 500)
    expectEqual(day2_distance['purpose_confirm_work'], 3000)


jest_describe("test_metrics_summaries")
