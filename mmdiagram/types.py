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
        """region address as hex"""
        self._size: str = size
        """size in bytes"""
        self.colour = self._pick_available_colour()
        """random colour for region block"""
        self.remain = self._calc_remaining()
        """Number of bytes until next region block"""

        # both 'lightslategray' and 'lightslategrey' are the same colour 
        # and we don't want duplicate colours in our diagram
        if "lightslategray" in Region._remaining_colours:
            del Region._remaining_colours["lightslategray"]

    @property
    def origin(self):
        """get region address as integer"""
        return int(self._origin, 16)

    @property
    def size(self):
        """get region size as integer"""
        return int(self._size, 16)

    def __str__(self):
        return "|"\
            + "<span style='color:" + str(self.colour) + "'>" + str(self.name) + "</span>|"\
            + str(self._origin) + "|"\
            + str(self._size) + "|"\
            + str(self.remain) + "|"

    def _pick_available_colour(self):
        # remove the picked colour from the list so it can't be picked again
        try:
            print(f"{self.name}:")
            # make sure we don't pick a colour that is too bright.
            # A0A0A0 was arbitrarily decided to be "too bright" :)
            chosen_colour_name, chosen_colour_code = random.choice(list(Region._remaining_colours.items()))
            while int(chosen_colour_code[1:], 16) > int("A0A0A0", 16):
                print(f"\tRejected {chosen_colour_name}({chosen_colour_code})")
                del Region._remaining_colours[chosen_colour_name]
                chosen_colour_name, chosen_colour_code = random.choice(list(Region._remaining_colours.items()))

            del Region._remaining_colours[chosen_colour_name]
            print(f"\tSelected {chosen_colour_name}({chosen_colour_code})")
        except (IndexError, KeyError):
            raise SystemExit("Ran out of colours!")
        print(f"\t### {len(Region._remaining_colours)} colours left ###")
        return chosen_colour_name

    def _calc_remaining(self):
        """Calculate the remaining number of bytes until next region block

        TODO iterate all other region blocks, determine which is nearest,
        calc the distance from origin + size of current region block

        Returns:
            None: TODO
        """
        return "TODO"
