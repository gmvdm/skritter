# -*- coding: utf-8 -*-
"""Example client for Skritter API

$ python example/client.py 'List title' exmaple/sample.csv

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
import sys

OAUTH_CLIENT_NAME = os.environ.get('SKRITTER_OAUTH_CLIENT_NAME')
OAUTH_CLIENT_SECRET = os.environ.get('SKRITTER_OAUTH_CLIENT_SECRET')


def get_new_words_from_file(filename, existing_words=None):
    words = []

    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = skritter.normalize(row[0].decode('utf-8'))

            if existing_words is not None and word in existing_words:
                continue

            words.append(word)

    return words


def get_next_section(sections):
    most_recent_date = 0
    most_recent_section = None
    for section in sections:
        if section['created'] > most_recent_date:
            most_recent_section = section

    if most_recent_section is None:
        most_recent_section = sections[-1]

    return most_recent_section


def add_word_ids_to_vocablist(s, vocablist, new_ids, max_section_size=200):
    ids_to_add = list(new_ids)

    next_section = get_next_section(vocablist['sections'])

    while len(ids_to_add) > 0:
        if len(next_section['rows']) >= max_section_size:
            # Add a new section
            new_section_name = 'Section %d' % (len(vocablist['sections']) + 1)
            vocablist['sections'].append({
                'name': new_section_name
                })
            vocablist = skritter.set_vocablist(s, vocablist)
            next_section = get_next_section(vocablist['sections'])

        section = skritter.get_vocab_section(s, vocablist['id'], next_section['id'])
        max_ids_for_section = max_section_size - len(section['rows'])
        ids_to_add_to_section = ids_to_add[:max_ids_for_section]

        for vocab_id in ids_to_add_to_section:
            section['rows'].append({'vocabId': vocab_id})

        next_section = skritter.set_vocab_section(s, vocablist['id'], section)

        ids_to_add = ids_to_add[max_ids_for_section:]

    # TODO(gmwils): determine which words were not added
    # TODO(gmwils): return indication of result of adding words


def main(user, password, list_name, filename):
    session = skritter.session(OAUTH_CLIENT_NAME, OAUTH_CLIENT_SECRET)
    session.login(user, password)

    vocablists = skritter.get_vocablists(session)
    vocablist_id = skritter.find_vocablist_by_name(vocablists, list_name)

    if vocablist_id is None:
        print 'Creating list: %s' % list_name
        # vocablist = create_vocablist(s, list_name, study_mode='adding')  # auto-study
        vocablist = skritter.create_vocablist(session, list_name)
        if not vocablist:
            print 'Unable to create list: %s' % list_name
            return
    else:
        vocablist = skritter.get_vocablist_details(session, vocablist_id)

    print 'Processing: %s' % vocablist['name']
    existing_words = skritter.get_vocablist_words(session, vocablist)
    print 'Found %d words in current list' % len(existing_words)
    new_words = get_new_words_from_file(filename, existing_words)

    unique_new_words = set(new_words)

    print 'Getting ids for %d new words to be added' % len(unique_new_words)
    new_word_ids, unknown_ids = skritter.get_ids_for_words(session, unique_new_words)

    print 'Adding %d unique word ids to %s' % (len(new_word_ids), vocablist['name'])
    add_word_ids_to_vocablist(session, vocablist, new_word_ids)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('usage: %s <list name> <filename>' % sys.argv[0])
    else:
        list_name = skritter.normalize(sys.argv[1].decode('utf-8'))
        filename = sys.argv[2]

    # TODO(gmwils): load these from the command line
    username = os.environ.get('SKRITTER_USER', 'iamuser')
    password = os.environ.get('SKRITTER_PASSWORD', 'secret')

    main(username, password, list_name, filename)
