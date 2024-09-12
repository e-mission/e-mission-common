export function merge_metadatas(meta_a: any, meta_b: any): void;
export function calc_footprint_for_trip(trip: any, label_options: any, mode_value: any, labels_map: any): Promise<any>;
export function calc_footprint(mode_footprint: any, distance: any, year: any, coords: any, uace: any, egrid_region: any, passengers: any, metadata: any): Promise<any>;
import * as emcmfe from './emcommon.metrics.footprint.egrid.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as Log from './emcommon.logger.js';
import * as emcdu from './emcommon.diary.util.js';
import * as emcmft from './emcommon.metrics.footprint.transit.js';
import * as emcmfu from './emcommon.metrics.footprint.util.js';
export { emcmfe, emcdb, Log, emcdu, emcmft, emcmfu };
//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.d.ts.map