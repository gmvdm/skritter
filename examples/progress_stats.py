# -*- coding: utf-8 -*-
"""Download user stats from Skritter as a CSV file

$ python examples/progress_stats.py filename

Note: requires environment variables set for OAuth client details,
      and for user authentication details.

eg.

export SKRITTER_OAUTH_CLIENT_NAME='<client name>'
export SKRITTER_OAUTH_CLIENT_SECRET='<client secret>'
export SKRITTER_USER='<username>''
export SKRITTER_PASSWORD='<password>'
"""

import csv
import datetime
import os
import skritter
import sys

OAUTH_CLIENT_NAME = os.environ.get('SKRITTER_OAUTH_CLIENT_NAME')
OAUTH_CLIENT_SECRET = os.environ.get('SKRITTER_OAUTH_CLIENT_SECRET')


def report_monthly_stats(session, start_date, end_date, output_file):
    progress_stats = skritter.get_progress_stats(session,
                                                 start_date,
                                                 end_date,
                                                 'month')
    with open(output_file, 'wb') as f:
        writer = csv.writer(f)
        header = ['date', 'client', 'days studied', 'time studied']
        for obj_type in ['word', 'char']:
            for val in ['defn', 'reading', 'rune', 'tone']:
                for study_type in ['learned', 'learning', 'remembered', 'studied']:
                    header += ['%s %s %s' % (obj_type, val, study_type)]

        writer.writerow(header)

        for month in progress_stats:
            data = []
            # Basic stats
            data.append(month.get('date'))
            data.append(month.get('client'))
            data.append(month['daysStudied']['all'])
            data.append(month['timeStudied']['all'])

            # Word stats
            word = month['word']
            for obj in [word['defn'], word['rdng'], word['rune'], word['tone']]:
                add_details(data, obj)

            # Character stats
            char = month['char']
            for obj in [char['defn'], char['rdng'], char['rune'], char['tone']]:
                add_details(data, obj)

            writer.writerow(data)


def add_details(data, obj):
    data.append(obj['learned']['all'])
    data.append(obj['learning']['all'])
    data.append(obj['remembered']['all'])
    data.append(obj['studied']['all'])


def main(username, password, filename):
    session = skritter.session(OAUTH_CLIENT_NAME, OAUTH_CLIENT_SECRET)
    session.login(username, password)

    today = datetime.date.today()
    days_ago = datetime.timedelta(731)  # max supported by API
    start_date = (today - days_ago).isoformat()
    end_date = today.isoformat()

    report_monthly_stats(session, start_date, end_date, filename)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        filename = 'output.csv'
    else:
        filename = sys.argv[1]

    # TODO(gmwils): load these from the command line
    username = os.environ.get('SKRITTER_USER', 'iamuser')
    password = os.environ.get('SKRITTER_PASSWORD', 'secret')

    main(username, password, filename)
