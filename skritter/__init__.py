# -*- coding: utf-8 -*-

"""
skritter client library
~~~~~~~~~~~~~~~~~~~~~~~
"""

__title__ = 'skritter'
__version__ = '0.1.0'
__author__ = 'Geoff van der Meer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Geoff van der Meer'

from .session import session, Session
from .utils import normalize
from .vocabs import get_ids_for_words
from .vocablists import (
    get_vocablists, get_vocablist_words, get_vocablist_details,
    get_vocab_section, set_vocab_section, create_vocablist,
    find_vocablist_by_name, set_vocablist)

