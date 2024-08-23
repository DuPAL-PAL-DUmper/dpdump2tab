"""Tests for truth table tools"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
import io
import os
sys.path.insert(0, './src') # Make VSCode happy...

import pytest

import dpdump2tab.ttable_tools as TTableTools


def test_write_ttable_header(ic_definition_PAL12x6):
    bw = io.BytesIO()
    TTableTools.write_truth_table_header(ic_definition_PAL12x6, bw)
    bw.seek(0, os.SEEK_SET)
    header: str = bw.read().decode(TTableTools._DEFAULT_ENCODING)

    assert header == '# PAL12x6\n.i 12 .o 6\n.ilb i1 i2 i3 i4 i5 i6 i7 i8 i9 i11 i12 i19\n.ob o13 o14 o15 o16 o17 o18\n.phase 000000\n'