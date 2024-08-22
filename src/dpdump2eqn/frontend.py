"""Frontend module"""

import argparse
import logging
from typing import List

from dpdump2eqn import __name__, __version__

from dpdumperlib.ic.ic_definition import ICDefinition
from dpdumperlib.ic.ic_loader import ICLoader

from dpdump2eqn.infile_utilities import load_file_data

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
    args = _build_argsparser().parse_args()

    # Prepare the logger
    debug_level: int = logging.ERROR
    if args.verbose > 1:
        debug_level = logging.DEBUG
    elif args.verbose > 0:
        debug_level = logging.INFO
    logging.basicConfig(level=debug_level)

    _LOGGER.info(f'Reading definition from {args.definition} and input data from {args.infile}')

    ic_definition: ICDefinition = ICLoader.extract_definition_from_file(args.definition)
    
    bytes_per_entry: int = -(len(ic_definition.data) // -8) # Calculate how many bytes are needed for a data entry
    addr_combs: int = 1 << len(ic_definition.address) # Calculate the number of addresses that this IC supports

    data: List[int] = load_file_data(args.infile, bytes_per_entry)

    if (d_len := len(data)) != addr_combs:
        raise ValueError(f'Input file has {d_len} entries, but {addr_combs} were expected!')

    return 0