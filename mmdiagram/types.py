import typeguard
import random
import PIL.ImageColor
from typing import List, Dict


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
        self.colour = self._pick_available_colour()
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
            + "<span style='color:" + str(self.colour) + "'>" + str(self.name) + "</span>|"\
            + str(self.origin) + "|"\
            + str(self.size) + "|"\
            + str(self.remain) + "|"

    def _pick_available_colour(self):
        # remove the picked colour from the list so it can't be picked again
        try:
            # make sure we don't pick a colour that is too bright.
            # A0A0A0 was arbitrarily decided to be "too bright" :)
            chosen_colour_name, chosen_colour_code = random.choice(list(Region._remaining_colours.items()))
            while int(chosen_colour_code[1:], 16) > int("A0A0A0", 16):
                del Region._remaining_colours[chosen_colour_name]
                chosen_colour_name, chosen_colour_code = random.choice(list(Region._remaining_colours.items()))

            del Region._remaining_colours[chosen_colour_name]
        except (IndexError, KeyError):
            raise SystemExit("Ran out of colours!")
        
        return chosen_colour_name

    def _calc_remaining(self):
        """Calculate the remaining number of bytes until next region block

        TODO iterate all other region blocks, determine which is nearest,
        calc the distance from origin + size of current region block

        Returns:
            None: TODO
        """
        return "TODO"
