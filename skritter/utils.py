# -*- coding: utf-8 -*-

import unicodedata


def normalize(string, normal_form='NFC'):
    """Normalize a unicode string for easy comparison."""
    if string is None:
        return None

    return unicodedata.normalize(normal_form, string)
