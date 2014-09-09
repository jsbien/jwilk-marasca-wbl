# encoding=UTF-8

# Copyright © 2013 Jakub Wilk <jwilk@jwilk.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import icu

Locale = icu.Locale
default_locale = Locale('en-US-POSIX')

def split(text, locale=default_locale):
    break_iterator = icu.BreakIterator.createWordInstance(locale)
    break_iterator.setText(text)
    i = 0
    for j in break_iterator:
        yield text[i:j]
        i = j

def split_bbox(text, bbox, locale=default_locale):
    x0, y0, x1, y1 = bbox
    w = x1 - x0
    break_iterator = icu.BreakIterator.createWordInstance(locale)
    break_iterator.setText(text)
    n = len(text)
    i = 0
    for j in break_iterator:
        subtext = text[i:j]
        subbbox = (
            x0 + w * i // n,
            y0,
            x0 + w * j // n,
            y1,
        )
        yield subtext, subbbox
        i = j

# vim:ts=4 sw=4 et