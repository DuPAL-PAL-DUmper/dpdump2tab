"""Frontend module"""

import argparse
import logging

from dpdump2eqn import __name__, __version__

_LOGGER: logging.Logger = logging.getLogger(__name__)

def _build_argsparser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog=__name__,
        description='A tool to convert dpdumper dumps to logic equations'
    )

    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    parser.add_argument('-d', '--definition',
                        metavar='definition file',
                        help='Path to the file containing the definition of the IC to be read',
                        required=True)
    
    parser.add_argument('-i', '--infile',
                        metavar='binary input file',
                        help='Path to the file binary data to be converted',
                        required=True)

    return parser

def cli() -> int:
    return 0