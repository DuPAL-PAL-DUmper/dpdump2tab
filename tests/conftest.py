"""Fixtures for testing"""

# pylint: disable=wrong-import-position

import sys
sys.path.insert(1, '.') # Make VSCode happy...

import pytest

from dpdumperlib.ic.ic_definition import ICDefinition
from dpdumperlib.ic.ic_loader import ICLoader

@pytest.fixture
def ic_definition_PAL12x6() -> ICDefinition:
    return ICLoader.extract_definition_from_file('tests/data/PAL12x6.toml')
