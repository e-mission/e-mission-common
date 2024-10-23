import unittest

import emcommon.metrics.footprint.util as emcmfu
import emcommon.metrics.footprint.transit as emcmft
import emcommon.diary.base_modes as emcdb

NYC_UACE_CODE = "63217"
CHICAGO_UACE_CODE = "16264"

BUS_MODES = emcdb.BASE_MODES['BUS']['footprint']['transit']
TRAIN_MODES = emcdb.BASE_MODES['TRAIN']['footprint']['transit']


class TestTransit(unittest.IsolatedAsyncioTestCase):
    async def test_get_uace_by_coords(self):
        cincinnati_uace_code = "16885"
        result = await emcmfu.get_uace_by_coords([-84.5, 39.1], 2022)
        self.assertEqual(result, cincinnati_uace_code)

    async def test_bus_nyc(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, NYC_UACE_CODE, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 641.24, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 22)

    async def test_bus_chicago(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, CHICAGO_UACE_CODE, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 1039.10, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 2)

    async def test_bus_nationwide(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, None, BUS_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 804.91, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 410)

    async def test_train_nyc(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, NYC_UACE_CODE, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 24.75, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 6)

    async def test_train_chicago(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, CHICAGO_UACE_CODE, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 158.14, places=2)
        # 3 passenger rail systems in Chicago - "the L", Metra, and South Shore Line
        self.assertEqual(len(metadata['ntd_ids']), 3)

    async def test_train_nationwide(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, None, TRAIN_MODES)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 67.87, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 49)

    async def test_all_modes_nationwide(self):
        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(2022, None, None)
        self.assertAlmostEqual(intensities['overall']['wh_per_km'], 483.04, places=2)
        self.assertEqual(len(metadata['ntd_ids']), 517)


class TestTransitCalculationsFakeData(unittest.IsolatedAsyncioTestCase):
    async def test_get_intensities_fake_data2(self):
        """
        Example scenario from:
        https://github.com/JGreenlee/e-mission-common/pull/2#issuecomment-2263813540
        """

        # Create a fake NTD data file for year 9999 and UACE code "99999"
        open("./src/emcommon/resources/ntd9999_intensities.json", "w").write("""
            {
                "records": [
                    {"NTD ID": "Agency A", "UACE Code": "99999", "Mode": "MB",
                    "Diesel (Wh/pkm)": 600, "Diesel (%)": 100,
                    "Unlinked Passenger Trips": 600},
                    {"NTD ID": "Agency A", "UACE Code": "99999", "Mode": "RB",
                    "Electric (Wh/pkm)": 500, "Electric (%)": 100,
                    "Unlinked Passenger Trips": 150},
                    {"NTD ID": "Agency B", "UACE Code": "99999", "Mode": "MB",
                    "Diesel (Wh/pkm)": 400, "Diesel (%)": 80,
                    "Electric (Wh/pkm)": 300, "Electric (%)": 20,
                    "Unlinked Passenger Trips": 250}
                ],
                "metadata": {
                    "year": 9999,
                    "data_source_urls": ["https://fake.url", "https://fake2.url"]
                }
            }
        """)

        (intensities, metadata) = await emcmft.get_transit_intensities_for_uace(9999, '99999', BUS_MODES)

        expected_intensities = {
            "diesel": {"wh_per_km": 550, "weight": 0.8},
            "electric": {"wh_per_km": 450, "weight": 0.2},
            "overall": {"wh_per_km": 530, "weight": 1.0},
        }
        expected_metadata = {
            "data_sources": ["ntd9999"],
            "data_source_urls": ["https://fake.url", "https://fake2.url"],
            "is_provisional": False,
            "requested_year": 9999,
            "ntd_uace_code": "99999",
            "ntd_modes": BUS_MODES,
            "ntd_ids": ["Agency A", "Agency B"],
        }
        self.assertDictEqual(intensities, expected_intensities)
        self.assertDictEqual(metadata, expected_metadata)

    # delete the fake data file when we're done
    def tearDown(self):
        import os
        try:
            os.remove("./src/emcommon/resources/ntd9999_intensities.json")
        except OSError:
            pass
