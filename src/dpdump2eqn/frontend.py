"""Frontend module"""

import argparse
import logging
from typing import List

from dpdump2eqn import __name__, __version__

from dpdumperlib.ic.ic_definition import ICDefinition
from dpdumperlib.ic.ic_loader import ICLoader
import dpdumperlib.io.file_utils as FileUtils

import logicmin

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

    data: List[int] = FileUtils.load_file_data(args.infile, bytes_per_entry)

    if (d_len := len(data)) != addr_combs:
        raise ValueError(f'Input file has {d_len} entries, but {addr_combs} were expected!')

    _LOGGER.info('Loading the truth table')
    tt: logicmin.TT = build_truth_table(ic_definition, data)

    # TODO: Solve the equations and print the solutions

    _LOGGER.info('Quitting.')
    return 1 

def build_truth_table(ic_definition: ICDefinition, data: List[int]) -> logicmin.TT:
    in_len: int = len(ic_definition.address)
    out_len: int = len(ic_definition.data)

    tt: logicmin.TT = logicmin.TT(in_len, out_len)

    _LOGGER.debug(f'Loading {len(data)} entries. Input width {in_len}, Output width {out_len}')
    for i, out in enumerate(data):
        tt.add(f'{i:0{in_len}b}', f'{out:0{out_len}b}')

    return tt