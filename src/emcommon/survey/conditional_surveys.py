from __future__ import annotations  # __: skip
import emcommon.logger as Log
import re  # __: skip


def point_is_within_bounds(pt: list, bounds: list[list]) -> bool:
    """
    Returns true if the given point is within the given bounds.
    Coordinates are in [longitude, latitude] order, since that is the GeoJSON spec.
    :param pt: point to check as [lon, lat]
    :param bounds: NW and SE corners as [[lon, lat], [lon, lat]]
    :return: True if pt is within bounds
    """
    # pt's lon must be east of, or greater than, NW's lon; and west of, or less than, SE's lon
    lon_in_range = pt[0] > bounds[0][0] and pt[0] < bounds[1][0]
    # pt's lat must be south of, or less than, NW's lat; and north of, or greater than, SE's lat
    lat_in_range = pt[1] < bounds[0][1] and pt[1] > bounds[1][1]
    return lat_in_range and lon_in_range


conditional_survey_fns = {
    'pointIsWithinBounds': point_is_within_bounds,
}


def scoped_eval(script: str, scope: dict) -> any:
    """
    Evaluate an expression in a restricted scope (implementations for both JS and Python)
    :example scoped_eval('foo + 1', { foo: 1 }) -> 2
    """
    # JS implementation (using literal JS code)
    '''?
    __pragma__('js', '{}', """
        return Function(...Object.keys(scope), `return ${script}`)(...Object.values(scope));
    """)
    ?'''

    # Python implementation
    return eval(script, scope)  # __: skip


def get_shows_if_condition(survey: dict) -> str:
    """
    Get the showsIf condition for a survey, considering both Python and JS implementations
    """
    # JS implementation
    '''?
    return survey['showsIf'];
    ?'''

    # Python implementation
    # __pragma__('skip')
    if 'showsIfPy' in survey:
        return survey['showsIfPy']
    expression = survey['showsIf']
    expression = expression.replace('&&', 'and')
    expression = expression.replace('||', 'or')
    expression = re.sub(r"!(?!=)", "not ", expression)
    return expression
    # __pragma__('noskip')


def survey_prompted_for_trip(composite_trip: dict, app_config: dict) -> str | None:
    """
    :param composite_trip: composite trip
    :param app_config: app config
    :return: the name of the survey that was prompted for the trip, or None if no survey was prompted
    """
    potential_surveys = None
    try:
        potential_surveys = app_config['survey_info']['buttons']['trip-label']
    except:
        Log.warn('No surveys in app config')
        return None
    # if potential surveys is not a list, just return it
    if not isinstance(potential_surveys, list):
        return potential_surveys['surveyName']
    for survey in potential_surveys:
        shows_if = get_shows_if_condition(survey)
        scope = dict(composite_trip)
        scope.update(conditional_survey_fns)

        # remove this once confirmedMode is not used anywhere
        shows_if = shows_if.replace('confirmedMode?.baseMode', 'primary_ble_sensed_mode')
        if 'primary_ble_sensed_mode' not in scope:
            try:
                scope['primary_ble_sensed_mode'] = scope['confirmedMode']['baseMode']
            except:
                scope['primary_ble_sensed_mode'] = None

        try:
            if scoped_eval(shows_if, scope):
                return survey['surveyName']
        # handles Python exception
        except Exception as e:
            Log.error(f"Error evaluating showsIf for survey {survey}: {e}")
        # handles JS exception
        except:
            Log.error(f"Error evaluating showsIf for survey {survey}: {__except0__}")
    # no survey passed its condition; return None
    return None
