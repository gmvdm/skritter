# -*- coding: utf-8 -*-

SKRITTER_PROGSTATS_URL = 'http://www.skritter.com/api/v0/progstats'


def get_progress_stats(session, start_date, end_date=None, step='day',
                       lang=None, fields=None):
    """
    Get the raw data on the user's progress.

    start_date - date of the beginning of range to fetch (required)
    end_date - date of the end of the range to fetch (default: start_date)
    step - 'day', 'week', or 'month'
    lang - language to fetch stats for (default: User setting)
    fields - comma separated list of fields to fetch (default: all)
    """
    params = {
        'start': start_date,
        'step': step,
        }

    if end_date is not None:
        params['end'] = end_date

    if lang is not None:
        params['lang'] = lang

    if fields is not None:
        params['fields'] = fields

    response = session.get(SKRITTER_PROGSTATS_URL, params=params)

    return response.get('ProgressStats')
