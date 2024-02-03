import typeguard
import random
import PIL.ImageColor
from typing import Dict

@typeguard.typechecked
class Region:

    _remaining_colours: Dict = PIL.ImageColor.colormap.copy()
    """Copy of the PIL colour string map, we remove colours until all are gone.
    Therefore avoiding random picking of duplicate colours"""

    def __init__(self, name: str, origin: str, size: str):

        self.name: str = name
        """region legend"""
        self._origin: str = origin
        """memory address"""
        self._size: str = size
        """size in bytes"""
        self.colour = self._pick_remainging_colour()
        """random colour for region block"""
        self.remain = self._calc_remaining()
        """Number of bytes until next region block"""

    @property
    def origin(self):
        return int(self._origin, 16)

    @origin.setter
    def origin(self, val):
        self._origin = val

    @property
    def size(self):
        return int(self._size, 16)

    def __str__(self):
        return "|"\
            + str(self.name) + "|"\
            + str(self.colour) + "|"\
            + str(self.origin) + "|"\
            + str(self.size) + "|"\
            + str(self.remain) + "|"

    def _pick_remainging_colour(self):
        # keep assigning colours to new objects until exhausted colourmap causes a KeyError
        if not Region._remaining_colours:
            raise KeyError("Run out of region colours!")
        chosen_colour = random.choice(list(Region._remaining_colours))
        del Region._remaining_colours[chosen_colour]
        return chosen_colour

    def _calc_remaining(self):
        """Calculate the remaining number of bytes until next region block

        TODO iterate all other region blocks, determine which is nearest,
        calc the distance from origin + size of current region block

        Returns:
            None: TODO
        """
        return "TODO"
