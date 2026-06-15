"""Seed utility functions to manage reproducibility across standard libraries."""

import random
import numpy as np

_GLOBAL_SEED = None


def set_global_seed(seed: int | None) -> None:
    """Set the global random seed for python's random and numpy.

    Args:
        seed: The integer seed to set. If None, the global seed is cleared.
    """
    global _GLOBAL_SEED
    _GLOBAL_SEED = seed
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)


def get_global_seed() -> int | None:
    """Get the current global seed.

    Returns:
        The current global seed, or None if not set.
    """
    return _GLOBAL_SEED
