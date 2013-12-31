# -*- coding: utf-8 -*-

from skritter.utils import normalize

import unicodedata
import unittest


class TestNormalize(unittest.TestCase):
    def test_none(self):
        self.assertEqual(None, normalize(None))

    def test_empty_string(self):
        self.assertEqual(u'', normalize(u''))

    def test_unicode_string(self):
        self.assertEqual(normalize(u'怀表'), unicodedata.normalize('NFC', u'怀表'))
