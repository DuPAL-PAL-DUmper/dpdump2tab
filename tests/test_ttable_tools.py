"""Tests for truth table tools"""

# pylint: disable=wrong-import-position,wrong-import-order

import sys
import io
import os
from typing import List
sys.path.insert(0, './src') # Make VSCode happy...

import pytest

import dpdump2tab.ttable_tools as TTableTools


def test_write_ttable_header(ic_definition_PAL12x6):
    bw = io.BytesIO()
    TTableTools.write_truth_table_header(ic_definition_PAL12x6, bw)
    bw.seek(0, os.SEEK_SET)
    header: str = bw.read().decode(TTableTools._DEFAULT_ENCODING)

    assert header == '# PAL12x6\n.i 12 .o 6\n.ilb i19 i12 i11 i9 i8 i7 i6 i5 i4 i3 i2 i1\n.ob o18 o17 o16 o15 o14 o13\n.phase 000000\n'

def test_write_ttable(ic_definition_PAL12x6):
    bw = io.BytesIO()
    data: List[int] = [i for i in range(1 << len(ic_definition_PAL12x6.address))]
    TTableTools.write_truth_table(ic_definition_PAL12x6, data, bw)
    bw.seek(0, os.SEEK_SET)
    table: str = bw.read().decode(TTableTools._DEFAULT_ENCODING)

    assert len(table) == 102464
   