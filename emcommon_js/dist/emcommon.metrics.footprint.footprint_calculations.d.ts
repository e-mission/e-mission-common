export function calc_footprint_for_trip(trip: any, label_options: any, mode_key: any, mode_value: any, labels_map: any): Promise<any>;
export function calc_footprint(mode_footprint: any, distance: any, year: any, coords: any, uace: any, egrid_region: any, passengers: any, metadata: any): Promise<any>;
export const _worst_rich_mode: any;
export const _worst_wh_per_km: number;
export function find_worst_rich_mode(label_options: any): any;
import * as emcdu from './emcommon.diary.util.js';
import * as emcmft from './emcommon.metrics.footprint.transit.js';
import * as emcmfe from './emcommon.metrics.footprint.egrid.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as Log from './emcommon.logger.js';
import * as emcmfu from './emcommon.metrics.footprint.util.js';
export { emcdu, emcmft, emcmfe, emcdb, Log, emcmfu };
//# sourceMappingURL=emcommon.metrics.footprint.footprint_calculations.d.ts.map