# -*- coding: utf-8 -*-

SKRITTER_VOCABS_URL = 'http://www.skritter.com/api/v0/vocabs'

import logging


logger = logging.getLogger(__name__)


def get_vocabs_for_ids(session, vocab_ids, fields=None, batch=50):
    logger.debug('get %d vocabs with fields "%s" in batches of %d',
                 len(vocab_ids), fields, batch)
    vocabs = []
    params = {}
    if fields:
        params['fields'] = fields

    to_fetch = list(vocab_ids)

    while to_fetch:
        subset = to_fetch[:batch]
        params['ids'] = '|'.join(subset)

        response = session.get(SKRITTER_VOCABS_URL, params=params)
        if response is not None:
            vocabs += response.get('Vocabs')

        to_fetch = to_fetch[batch:]

    return vocabs


def get_vocabs_for_query(session, query, fields=None, limit=1):
    params = {}
    params['limit'] = limit
    if fields:
        params['fields'] = fields

    params['q'] = query

    response = session.get(SKRITTER_VOCABS_URL, params=params)

    if response:
        return response.get('Vocabs')
    else:
        logger.error('Unable to retrieve vocabs for query: %s', query)
        return None


def get_ids_for_words(session, new_words):
    '''Given a list of words, return Skritter ids for those words, and words not found'''
    ids = set()
    unknown_words = set()

    for word in new_words:
        vocabs = get_vocabs_for_query(session, word, 'id,style,lang,writing')
        id_found = False

        if vocabs is None:
            unknown_words.add(word)
            continue

        for vocab in vocabs:
            # Two vocabs often come back, one with 'simp' and one with 'trad'
            # TODO(gmwils): support user preference of simp, trad & both
            if vocab['style'] in ['simp', 'both']:
                ids.add(vocab['id'])
                id_found = True

        if not id_found:
            unknown_words.add(word)

    return ids, unknown_words
