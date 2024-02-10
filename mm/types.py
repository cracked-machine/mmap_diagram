import typeguard
import random
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
from typing import List, Dict
import logging


@typeguard.typechecked
class Region():
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
        self.bordercolour = "black"
        """The border colour to use for the region"""
        self.remain: str = None
        """Number of bytes until next region block"""
        self.collisons: Dict(str, str) = {}
        """Map of collision regions by name (str) and distance (hex)"""
        self.draw_indent = 0
        """Index counter for incrementally shrinking the drawing indent"""

        self.img: PIL.Image

        # both 'lightslategray' and 'lightslategrey' are the same colour
        # and we don't want duplicate colours in our diagram
        if "lightslategray" in MemoryRegion._remaining_colours:
            del MemoryRegion._remaining_colours["lightslategray"]

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
            + str(self.remain) + "|"\
            + str(self.collisons) + "|"

    def _pick_available_colour(self):
        # remove the picked colour from the list so it can't be picked again
        try:
            logging.debug(f"{self.name}:")
            # make sure we don't pick a colour that is too bright.
            # A0A0A0 was arbitrarily decided to be "too bright" :)
            chosen_colour_name, chosen_colour_code = random.choice(list(MemoryRegion._remaining_colours.items()))
            while int(chosen_colour_code[1:], 16) > int("A0A0A0", 16):
                logging.debug(f"\tRejected {chosen_colour_name}({chosen_colour_code})")
                del MemoryRegion._remaining_colours[chosen_colour_name]
                chosen_colour_name, chosen_colour_code = random.choice(list(MemoryRegion._remaining_colours.items()))

            del MemoryRegion._remaining_colours[chosen_colour_name]
            logging.debug(f"\tSelected {chosen_colour_name}({chosen_colour_code})")
        except (IndexError, KeyError):
            raise SystemExit("Ran out of colours!")
        logging.debug(f"\t### {len(MemoryRegion._remaining_colours)} colours left ###")
        return chosen_colour_name

    def calc_nearest_region(self, region_list: List['MemoryRegion'], diagram_height: int):
        """Calculate the remaining number of bytes until next region block"""
        
        region_distances = {}
        logging.debug(f"Calculating nearest distances to {self.name} region:")
        this_region_end = 0

        for probed_region in region_list:
            # calc the end address of this and inspected region
            this_region_end: int = self.origin + self.size
            probed_region_end: int = probed_region.origin + probed_region.size

            # skip calculating distance from yourself.
            if self.name == probed_region.name:
                continue

            # skip if 'this' region origin is ahead of the probed region end address
            if self.origin > probed_region_end:
                continue

            probed_region_distance: int = probed_region.origin - this_region_end
            logging.debug(f"\t{hex(probed_region_distance)} bytes to {probed_region.name}")

            # collision detected
            if probed_region_distance < 0:
                # was the region that collided into us at a lower or higher origin address
                if probed_region.origin < self.origin:
                    # lower so use our origin address as the collion point
                    self.collisons[probed_region.name] = hex(self.origin)
                else:
                    # higher so use their origin address as the collion point
                    self.collisons[probed_region.name] = hex(probed_region.origin)

                if self.origin < probed_region.origin:
                    # no distance left
                    self.remain = hex(probed_region_distance)
                    pass

            else:
                # record the distance for later
                region_distances[probed_region.name] = probed_region_distance
                # set a first value while we have it (in case there are no future collisions)
                if not self.remain and not self.collisons:
                    self.remain = hex(probed_region_distance)
                # # if remain not already set to no distance left then set the positive remain distance
                elif not self.remain:
                    self.remain = hex(probed_region_distance)

        logging.debug(f"Non-collision distances - {region_distances}")
        # after probing each region we must now pick the lowest distance ()
        if not self.collisons:
            if region_distances:
                lowest = min(region_distances, key=region_distances.get)
                self.remain = hex(region_distances[lowest])
            else:
                self.remain = hex(diagram_height - this_region_end)
        elif self.collisons and not self.remain:
            self.remain = hex(diagram_height - this_region_end)


@typeguard.typechecked
class MemoryRegion(Region):

    def create_img(self, img_width: int, font_size: int):

        logging.info(self)
        if not self.size:
            logging.warning("Zero size region skipped")
            return None

        # MemoryRegion Blocks and text
        region_img = PIL.Image.new("RGBA", (img_width, self.size), color="white")
        self.region_canvas = PIL.ImageDraw.Draw(region_img)

        # height is -1 to avoid clipping the top border
        self.region_canvas.rectangle(
            (0, 0, img_width, self.size - 1),
            fill=self.colour,
            outline=self.bordercolour,
            width=1,
        )

        # draw name text
        region_img.paste(TextLabel(text=self.name, font_size=font_size).img, (5, 5))

        self.img = region_img


@typeguard.typechecked
class VoidRegion(Region):

    def __init__(self, size: str):

        self.name: str = "~~~~~ SKIPPED ~~~~~"
        
        super().__init__(self.name, "0x0", size)

    def create_img(self, img_width: int, font_size: int):

        logging.info(self)
        if not self.size:
            logging.warning("Zero size region skipped")
            return None

        # MemoryRegion Blocks and text
        region_img = PIL.Image.new("RGBA", (img_width + 1, self.size), color="white")
        self.region_canvas = PIL.ImageDraw.Draw(region_img)

        # height is -1 to avoid clipping the top border
        self.region_canvas.rectangle(
            (0, 0, img_width, self.size - 1),
            fill="oldlace",
            outline="black",
            width=1,
        )

        # draw name text
        region_w, region_h = region_img.size
        region_img.paste(TextLabel(text=self.name, font_size=font_size).img, (region_w // 5, region_h // 3))

        self.img = region_img


@typeguard.typechecked
class TextLabel():
    def __init__(self, text: str, font_size: int):
        self.text = text
        """The display label text"""

        self.font = PIL.ImageFont.load_default(font_size)
        """The font used to display the text"""

        _, top, right, bottom = self.font.getbbox(self.text)
        """The dimensions required for the text"""
        
        self.width = right
        """The label width"""

        self.height = bottom - top
        """The label height"""

        self.bgcolour = "oldlace"
        """The background colour to use for the region text label"""

        self.fgcolour = "black"
        """The foreground colour to use for the region text label"""

        self.img: PIL.Image
        """The image object. Use this with PIL.Image.paste()"""

        self._create_img()

    def _create_img(self):

        # make the image bigger than the actual text bbox so there is plenty of space for the text
        self.img = PIL.Image.new("RGB", (self.width * 2, self.height * 2), color=self.bgcolour)
        canvas = PIL.ImageDraw.Draw(self.img)
        # center the text in the oversized image, bias the y-pos by 1/5
        canvas.text(xy=(self.width / 2, (self.height / 2 - (self.height / 5))),
                    text=self.text,
                    fill=self.fgcolour,
                    font=self.font)

        # the final diagram image will be flipped so start with the text upside down
        self.img = self.img.rotate(180)
