# -*- coding: utf-8 -*-

SKRITTER_VOCABLIST_URL = 'http://www.skritter.com/api/v0/vocablists'

from .utils import normalize
from .vocabs import get_vocabs_for_ids

import logging


logger = logging.getLogger(__name__)


def create_vocablist(s, vocablist_name, vocablist_desc=None,
                     study_mode='not studying'):
    params = {'gzip': 'false'}

    vocablist = {
        'name': vocablist_name,
        'lang': 'zh',
        'tags': [],
        'studyingMode': study_mode,
        'sections': [{'name': 'Section 1'}],
        }

    if vocablist_desc:
        vocablist['description'] = vocablist_desc

    response = s.post_json(SKRITTER_VOCABLIST_URL, vocablist, params=params)

    return response.get('VocabList', None)


def get_vocablists(s):
    params = {
        'sort': 'custom'
        }
    response = s.get(SKRITTER_VOCABLIST_URL, params=params)

    return response.get('VocabLists', None)


def find_vocablist_by_name(vocablists, list_name):
    """ Given a collection of vocablists, find one by name"""
    list_name = normalize(list_name)
    vocablist_id = None

    if vocablists is None:
        return vocablist_id

    for vocablist in vocablists:
        if list_name == normalize(vocablist['name']):
            vocablist_id = vocablist['id']
            break

    return vocablist_id


def get_vocablist_details(s, list_id):
    vocablist_url = '%s/%s' % (SKRITTER_VOCABLIST_URL, list_id)
    response = s.get(vocablist_url)

    return response.get('VocabList', None)


def get_vocablist_vocab_ids(s, vocablist):
    vocab_ids = set()
    for section in vocablist['sections']:
        for row in section['rows']:
            vocab_ids.add(row['vocabId'])

    return vocab_ids


def get_vocablist_words(s, vocablist, batch=40):
    logger.debug('get words for skritter list id: %s', vocablist.get('id', 'no-list'))
    vocab_ids = get_vocablist_vocab_ids(s, vocablist)
    vocabs = get_vocabs_for_ids(s, vocab_ids, 'id,writing', batch)

    words = set()
    for entry in vocabs:
        words.add(entry['writing'])

    return words


def set_vocablist(s, vocablist):
    vocablist_url = '%s/%s' % (SKRITTER_VOCABLIST_URL, vocablist['id'])
    params = {'gzip': 'false'}

    response = s.put_json(vocablist_url, vocablist, params=params)

    return response.get('VocabList', None)


def get_vocab_section(s, vocablist_id, section_id):
    url = build_vocab_section_url(vocablist_id, section_id)
    response = s.get(url)

    return response.get('VocabListSection')


def set_vocab_section(s, vocablist_id, section):
    url = build_vocab_section_url(vocablist_id, section['id'])

    params = {'gzip': 'false'}

    response = s.put_json(url, section, params=params)

    return response.get('VocablistSection')


def build_vocab_section_url(vocablist_id, section_id,
                            vocablist_url=SKRITTER_VOCABLIST_URL):
    url = '%s/%s/sections/%s'
    url = url % (vocablist_url, vocablist_id, section_id)
    return url
