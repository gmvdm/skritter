# -*- coding: utf-8 -*-
"""Download user stats from Skritter

$ python example/download_stats.py

Note: requires environment variables set for OAuth client details,
      and for user authentication details.

eg.

export SKRITTER_OAUTH_CLIENT_NAME='<client name>'
export SKRITTER_OAUTH_CLIENT_SECRET='<client secret>'
export SKRITTER_USER='<username>''
export SKRITTER_PASSWORD='<password>'
"""

import csv
import os
import skritter

OAUTH_CLIENT_NAME = os.environ.get('SKRITTER_OAUTH_CLIENT_NAME')
OAUTH_CLIENT_SECRET = os.environ.get('SKRITTER_OAUTH_CLIENT_SECRET')


def main(username, password):
    session = skritter.session(OAUTH_CLIENT_NAME, OAUTH_CLIENT_SECRET)
    session.login(username, password)

    start_date = '2014-05-01'
    progress_stats = skritter.get_progress_stats(start_date, 'day')
    print progress_stats


if __name__ == '__main__':
    # TODO(gmwils): load these from the command line
    username = os.environ.get('SKRITTER_USER', 'iamuser')
    password = os.environ.get('SKRITTER_PASSWORD', 'secret')

    main(username, password)
