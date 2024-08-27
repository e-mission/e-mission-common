from __future__ import annotations  # __: skip
import emcommon.logger as Log
from emcommon.diary.base_modes import BASE_MODES


def get_mets_mode_map(label_options):
    """
    Gets a mapping of modes to their METs, given label options
    :param label_options: label options dict (from dynamic config 'label_options')
    :return: a dict of modes to their METs
    """
    mode_options = label_options['MODE']
    mode_met_entries = {}
    for opt in mode_options:
        if 'met' in opt:
            curr_met = opt['met']
        elif 'met_equivalent' in opt:
            curr_met = BASE_MODES[opt['met_equivalent']]['met']
        else:
            Log.warn(f'Did not find either met_equivalent or met for {opt["value"]} ignoring entry')
            continue
        for range_name in curr_met:
            # For custom METs, ranges can be specified. Sometimes we want open-ended ranges,
            # but JSON doesn't have a built-in way to represent "infinity" or "MAX_VALUE".
            # Any value that isn't >= 0 (e.g. -1, 'MAX', 'Inf') will be mapped to
            # float('inf')
            curr_met[range_name]['range'] = [
                i if isinstance(i, (int, float)) and i >= 0 else float('inf')
                for i in curr_met[range_name]['range']
            ]
        mode_met_entries[opt['value']] = curr_met
    return mode_met_entries
