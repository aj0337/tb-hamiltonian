from __future__ import annotations

import typing as t
from pathlib import Path

import numpy as np
from ase import Atoms
from ase.io import read


def get_structure(
    unit_cell_filepath: Path = Path("."),
    unit_cell_file_format: str = "vasp",
    repetitions: t.Tuple[int, int, int] | None = None,
    lengths: t.Tuple[float, float, float] | None = None,
    structure_filepath: Path = Path("."),
    structure_file_format: str = "vasp",
) -> Atoms:
    """Create a sorted structure object.

    Create a structure object from a unit cell, optionally extended by
    repetitions provided or derived from provided lengths. Alternatively,
    create a structure directly from a provided file. In either case,
    atoms are sorted by x, y, z, in order.

    Parameters
    ----------
    `unit_cell_filepath` : `Path`, optional
        Path to the unit cell file.
    `unit_cell_file_format` : `str`, optional
        File format of the unit cell file.
    `repetitions` : `tuple[int, int, int]`, optional
        Number of repetitions in the x, y, z directions.
    `lengths` : `tuple[float, float, float]`, optional
        Lengths of the supercell in the x, y, z directions.
    `structure_filepath` : `Path`, optional
        Path to the structure file.
    `structure_file_format` : `str`, optional
        File format of the structure file.

    Returns
    -------
    `ase.Atoms`
        Structure as `ase.Atoms` object with atoms sorted
        by x, y, and z, in order.
    """
    if unit_cell_filepath:
        unit_cell = read(unit_cell_filepath, format=unit_cell_file_format)
        if repetitions is not None:
            nx, ny, nz = repetitions
            return unit_cell.repeat((nx, ny, nz))  # type: ignore
        elif lengths is not None:
            nx, ny, nz = lengths // unit_cell.cell.lengths()  # type: ignore
            return unit_cell.repeat([int(i) for i in (nx, ny, nz)])  # type: ignore
        else:
            return sort_atoms(unit_cell)  # type: ignore
    elif structure_filepath:
        try:
            structure = read(structure_filepath, format=structure_file_format)
            return sort_atoms(structure)  # type: ignore
        except Exception as err:
            raise err
    else:
        raise ValueError("Either `unit_cell` or `structure_filepath` must be provided.")


def sort_atoms(atoms):
    """Sort atoms by their positions in the x, y, z directions.

    Parameters
    ----------
    `atoms` : `ase.Atoms`
        Atoms object to be sorted.

    Returns
    -------
    `ase.Atoms`
        Sorted Atoms object.
    """
    return atoms[
        np.lexsort(
            (
                atoms.positions[:, 0],
                atoms.positions[:, 1],
                atoms.positions[:, 2],
            )
        )
    ]
