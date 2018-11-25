def human_interval_to_seconds(val, units):
    assert units in [
            'second', 'seconds',
            'minute', 'minutes',
            'hour',   'hours',
            'day',    'days',
            'week',   'weeks',
            'month',  'months'
        ]

    result = 0 # seconds

    if units in ['second', 'seconds']:
        result = val
    elif units in ['minute', 'minutes']:
        result = val*60
    elif units in ['hour', 'hours']:
        result = val*60*60
    elif units in ['day', 'days']:
        result = val*60*60*24
    elif units in ['week', 'weeks']:
        result = val*60*60*24*7
    elif units in ['month', 'months']:
        result = val*60*60*24*30

    return result

def rev_dict(d):
    return { v: k for k, v in d.items() }

def as_list(arg):
    if not isinstance(arg, collections.Iterable):
        return [arg]
    else:
        return arg
