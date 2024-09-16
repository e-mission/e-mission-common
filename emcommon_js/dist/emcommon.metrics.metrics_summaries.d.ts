export const app_config: any;
export const labels_map: any;
export function generate_summaries(metric_list: any, trips: any, _app_config: any, _labels_map: any): Promise<{}>;
export function value_of_metric_for_trip(metric_name: any, grouping_field: any, grouping_val: any, trip: any): Promise<any>;
export function acc_value_of_metric(metric_name: any, acc: any, new_val: any): any;
export function get_summary_for_metric(metric: any, confirmed_trips: any): Promise<any[]>;
export const grouping_field_fns: {};
export function metric_summary_for_trips(metric: any, confirmed_trips: any): Promise<{}>;
import * as emcsc from './emcommon.survey.conditional_surveys.js';
import * as emcdb from './emcommon.diary.base_modes.js';
import * as emcble from './emcommon.bluetooth.ble_matching.js';
import * as emcmff from './emcommon.metrics.footprint.footprint_calculations.js';
import * as emcfu from './emcommon.metrics.footprint.util.js';
import * as emcdu from './emcommon.diary.util.js';
import * as util from './emcommon.util.js';
import * as Log from './emcommon.logger.js';
export { emcsc, emcdb, emcble, emcmff, emcfu, emcdu, util, Log };
//# sourceMappingURL=emcommon.metrics.metrics_summaries.d.ts.map