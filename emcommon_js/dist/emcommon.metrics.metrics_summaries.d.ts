export const app_config: any;
export const labels_map: any;
export function label_for_trip(composite_trip: any, label_key: any): any;
export function survey_answered_for_trip(composite_trip: any): any;
export function generate_summaries(metric_list: any, trips: any, _app_config: any, _labels_map: any): {};
export function value_of_metric_for_trip(metric_name: any, grouping_field: any, trip: any): any;
export function get_summary_for_metric(metric: any, confirmed_trips: any): any[];
export const grouping_field_fns: {};
export function metric_summary_for_trips(metric: any, confirmed_trips: any): {};
import * as emcsc from './emcommon.survey.conditional_surveys.js';
import * as emcble from './emcommon.bluetooth.ble_matching.js';
import * as Log from './emcommon.logger.js';
import * as util from './emcommon.util.js';
export { emcsc, emcble, Log, util };
//# sourceMappingURL=emcommon.metrics.metrics_summaries.d.ts.map