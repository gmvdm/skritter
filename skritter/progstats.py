# -*- coding: utf-8 -*-

SKRITTER_VOCABS_URL = 'http://www.skritter.com/api/v0/progstats'


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
    return None
