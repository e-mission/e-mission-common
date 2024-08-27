import fs from 'fs';

import { get_uace_by_coords } from '../../emcommon_js/emcommon.metrics.footprint.util';
import * as emcft from '../../emcommon_js/emcommon.metrics.footprint.transit';
import * as emcdb from '../../emcommon_js/emcommon.diary.base_modes';


const NYC_UACE_CODE = '63217';
const CHICAGO_UACE_CODE = '16264';

const BUS_MODES = emcdb.BASE_MODES['BUS']['footprint']['transit'];
const TRAIN_MODES = emcdb.BASE_MODES['TRAIN']['footprint']['transit'];


describe('TestTransit', () => {
  it('test_get_uace_by_zipcode', async () => {
    const cincinnati_uace_code = '16885';
    const result = await get_uace_by_coords([-84.5, 39.1], 2022);
    expect(result).toEqual(cincinnati_uace_code);
  });

  it('test_bus_nyc', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, NYC_UACE_CODE, BUS_MODES);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(646.80, 2);
    expect(metadata['ntd_ids'].length).toEqual(22);
  });
  
  it('test_bus_chicago', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, CHICAGO_UACE_CODE, BUS_MODES);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(1048.12, 2);
    expect(metadata['ntd_ids'].length).toEqual(2);
  });

  it('test_bus_nationwide', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, null, BUS_MODES);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(811.85, 2);
    expect(metadata['ntd_ids'].length).toEqual(410);
  });

  it('test_train_nyc', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, NYC_UACE_CODE, TRAIN_MODES);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(24.79, 2);
    expect(metadata['ntd_ids'].length).toEqual(6);
  });

  it('test_train_chicago', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, CHICAGO_UACE_CODE, TRAIN_MODES);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(159.04, 2);
    expect(metadata['ntd_ids'].length).toEqual(3);
  });

  it('test_train_nationwide', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, null, TRAIN_MODES);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(68.06, 2);
    expect(metadata['ntd_ids'].length).toEqual(49);
  });

  it('test_all_modes_nationwide', async () => {
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(2022, null, null);
    expect(intensities['overall']['wh_per_km']).toBeCloseTo(486.96, 2);
    expect(metadata['ntd_ids'].length).toEqual(517);
  });
});

describe('TestTransitCalculationsFakeData', () => {
  it('test_get_intensities_fake_data2', async () => {
    /* Example scenario from:
      https://github.com/JGreenlee/e-mission-common/pull/2#issuecomment-2263813540
    */
    // Create a fake NTD data file for year 9999 and UACE code "99999"
    const fake_data = {
      records: [
        {
          'NTD ID': 'Agency A',
          'UACE Code': '99999',
          'Mode': 'MB',
          'Diesel (Wh/pkm)': 600,
          'Diesel (%)': 100,
          'Unlinked Passenger Trips': 600,
        },
        {
          'NTD ID': 'Agency A',
          'UACE Code': '99999',
          'Mode': 'RB',
          'Electric (Wh/pkm)': 500,
          'Electric (%)': 100,
          'Unlinked Passenger Trips': 150,
        },
        {
          'NTD ID': 'Agency B',
          'UACE Code': '99999',
          'Mode': 'MB',
          'Diesel (Wh/pkm)': 400,
          'Diesel (%)': 80,
          'Electric (Wh/pkm)': 300,
          'Electric (%)': 20,
          'Unlinked Passenger Trips': 250,
        },
      ],
      metadata: {
        year: 9999,
        data_source_urls: ['https://fake.url', 'https://fake2.url'],
      },
    };
    fs.writeFileSync('./src/emcommon/resources/ntd9999_intensities.json', JSON.stringify(fake_data));

    console.log({cwd: process.cwd()});
    const [intensities, metadata] = await emcft.get_transit_intensities_for_uace(9999, '99999', BUS_MODES);

    const expected_intensities = {
      diesel: { wh_per_km: 550, weight: 0.8 },
      electric: { wh_per_km: 450, weight: 0.2 },
      overall: { wh_per_km: 530, weight: 1.0 },
    };
    const expected_metadata = {
      data_sources: ['ntd9999'],
      data_source_urls: ['https://fake.url', 'https://fake2.url'],
      is_provisional: false,
      requested_year: 9999,
      ntd_uace_code: '99999',
      ntd_modes: BUS_MODES,
      ntd_ids: ['Agency A', 'Agency B'],
    };
    expect(intensities).toEqual(expected_intensities);
    expect(metadata).toEqual(expected_metadata);
  });
});
