import * as emcmfe from "../../emcommon_js/emcommon.metrics.footprint.egrid";


const KG_PER_LB = 0.453592;

/*
eGRID expected values (collected from https://www.epa.gov/egrid/data-explorer)
"I want to explore <output emission rates(lb/MWh)> for <CO₂ equivalent> for <all fuels>
at the <eGRID subregion> level for <2022>."
*/
const EGRID_EXPECTED_LBS_PER_KWH = {
  'RFCW': 1005.90,
  'NWPP': 605.87,
};


describe('TestEgrid', () => {
  it('test_get_egrid_intensity_cincinnati_2022', async () => {
    const coords = [-84.52, 39.13];
    const [kg_per_kwh, metadata] = await emcmfe.get_egrid_intensity_for_coords(2022, coords);

    const expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["RFCW"] * KG_PER_LB;
    const expected_metadata = {
      "data_sources": ["egrid2022"],
      "data_source_urls": [
        "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
      ],
      "is_provisional": false,
      "requested_year": 2022,
      "requested_coords": coords,
      "egrid_region": "RFCW",
    };
    expect(kg_per_kwh).toBeCloseTo(expected_kg_per_kwh, 2);
    expect(metadata).toEqual(expected_metadata);
  });

  it('test_get_egrid_intensity_eagle_point_2023', async () => {
    const coords = [-122.83, 42.29];
    const [kg_per_kwh, metadata] = await emcmfe.get_egrid_intensity_for_coords(2023, coords);

    const expected_kg_per_kwh = EGRID_EXPECTED_LBS_PER_KWH["NWPP"] * KG_PER_LB;
    const expected_metadata = {
      "data_sources": ["egrid2022"],
      "data_source_urls": [
        "https://www.epa.gov/system/files/documents/2024-01/egrid2022_data.xlsx",
      ],
      "is_provisional": true,
      "requested_year": 2023,
      "requested_coords": coords,
      "egrid_region": "NWPP",
    };
    expect(kg_per_kwh).toBeCloseTo(expected_kg_per_kwh, 2);
    expect(metadata).toEqual(expected_metadata);
  });
});
