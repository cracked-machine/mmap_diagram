import typeguard
import random
import PIL.ImageColor
from typing import List, Dict
import mmdiagram.generator

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
        self.remain: str = None
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

    def calc_nearest_region(self, region_list: List['Region']):
        """Calculate the remaining number of bytes until next region block

        TODO iterate all other region blocks, determine which is nearest,
        calc the distance from origin + size of current region block
        

        Returns:
            None: TODO
        """
        region_distances = {}
        print(f"Calculating distances for {self.name}:")
        this_region_end = 0
        for next_region in region_list:
            # skip calculating distance from yourself.
            if self.name == next_region.name:
                continue
            this_region_end: int = self.origin + self.size
            next_region_end: int = next_region.origin + next_region.size
            if self.origin > next_region_end:
                continue
            next_region_distance: int = next_region.origin - this_region_end
            print(f"\t{next_region_distance} to {next_region.name}")
            if next_region_distance >= 0:
                region_distances[next_region.name] = next_region_distance
        
        print(region_distances)
        if region_distances:
            lowest = min(region_distances, key=region_distances.get)
            self.remain = hex(region_distances[lowest])
        else:
            self.remain = hex(mmdiagram.generator.height - this_region_end)
        return "TODO"
