# -*- coding: utf-8 -*-

SKRITTER_VOCABS_URL = 'http://www.skritter.com/api/v0/vocabs'


def get_vocabs_for_ids(session, vocab_ids, fields=None):
    vocabs = []
    params = {}
    if fields:
        params['fields'] = fields

    to_fetch = list(vocab_ids)

    while to_fetch:
        subset = to_fetch[:50]
        params['ids'] = '|'.join(subset)

        response = session.get(SKRITTER_VOCABS_URL, params=params)
        vocabs += response.get('Vocabs')

        to_fetch = to_fetch[50:]

    return vocabs


def get_vocabs_for_query(session, query, fields=None, limit=1):
    params = {}
    params['limit'] = limit
    if fields:
        params['fields'] = fields

    params['q'] = query

    response = session.get(SKRITTER_VOCABS_URL, params=params)

    return response.get('Vocabs')


def get_ids_for_words(session, new_words):
    ids = set()

    for word in new_words:
        vocabs = get_vocabs_for_query(session, word, 'id,style,lang,writing')
        for vocab in vocabs:
            # Two vocabs often come back, one with 'simp' and one with 'trad'
            # TODO(gmwils): support user preference of simp, trad & both
            if vocab['style'] == 'simp':
                ids.add(vocab['id'])

    return ids
