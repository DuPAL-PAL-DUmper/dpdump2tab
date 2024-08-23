"""This module contains utility code to generate espresso's truth tables"""

from io import BufferedIOBase
from typing import List

from dpdumperlib.ic.ic_definition import ICDefinition

_DEFAULT_ENCODING: str = 'ascii'

def write_truth_table_header(ic_definition: ICDefinition, bw: BufferedIOBase, phase_invert: bool = False) -> None:
    i_labels: List[str] = [f'i{pin}' for pin in ic_definition.nr_address]
    o_labels: List[str] = [f'o{pin}' for pin in ic_definition.nr_data]
    in_width: int = len(ic_definition.nr_address)
    out_width:int = len(ic_definition.nr_data)

    bw.write(f'# {ic_definition.name}\n'.encode(_DEFAULT_ENCODING))
    bw.write(f'.i {in_width} .o {out_width}\n'.encode(_DEFAULT_ENCODING))
    bw.write(f'.ilb {' '.join(i_labels)}\n'.encode(_DEFAULT_ENCODING))
    bw.write(f'.ob {' '.join(o_labels)}\n'.encode(_DEFAULT_ENCODING))
    bw.write(f'.phase {('1' if phase_invert else '0')*out_width}\n'.encode(_DEFAULT_ENCODING))