import typeguard
import random
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
from typing import List, Dict
import logging

import mm.diagram 

@typeguard.typechecked
class RegionImage:
    _remaining_colours: Dict = PIL.ImageColor.colormap.copy()
    """Copy of the PIL colour string map, we remove colours until all are gone.
    Therefore avoiding random picking of duplicate colours"""

    def __init__(self, parent: str, name: str):

        self.parent: str = parent
        """The name of the mm.metamodel.MemoryMap parent of this region"""

        self.name: str = name
        """region name"""

        self.colour = self._pick_available_colour()
        """random colour for region block"""

        self.bordercolour = "black"
        """The border colour to use for the region"""

        self.draw_indent = 0
        """Index counter for incrementally shrinking the drawing indent"""

        self.img: PIL.Image

        # both 'lightslategray' and 'lightslategrey' are the same colour
        # and we don't want duplicate colours in our diagram
        if "lightslategray" in MemoryRegionImage._remaining_colours:
            del MemoryRegionImage._remaining_colours["lightslategray"]

    @property
    def origin_as_hex(self):
        """ lookup memory_region_origin from metamodel  """
        return hex(mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].memory_region_origin)

    @property
    def size_as_hex(self):
        """ lookup memory_region_size from metamodel  """
        return hex(mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].memory_region_size)

    @property
    def freespace_as_hex(self):
        """ lookup memory_region freespace from metamodel  """
        return hex(mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].freespace)

    @property
    def origin_as_int(self):
        """ lookup memory_region_origin from metamodel  """
        return mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].memory_region_origin

    @property
    def size_as_int(self):
        """ lookup memory_region_size from metamodel  """
        return mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].memory_region_size

    @property
    def freespace_as_int(self):
        """ lookup memory_region freespace from metamodel  """
        return mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].freespace


    @property
    def collisions(self):
        """ lookup memory_region collision from metamodel  """
        return mm.diagram.Diagram.model.memory_maps[self.parent].memory_regions[self.name].collisions


    def _pick_available_colour(self):
        # remove the picked colour from the list so it can't be picked again
        try:
            logging.debug(f"{self.name}:")
            # make sure we don't pick a colour that is too bright.
            # A0A0A0 was arbitrarily decided to be "too bright" :)
            chosen_colour_name, chosen_colour_code = random.choice(list(MemoryRegionImage._remaining_colours.items()))
            while int(chosen_colour_code[1:], 16) > int("A0A0A0", 16):
                logging.debug(f"\tRejected {chosen_colour_name}({chosen_colour_code})")
                # del MemoryRegionImage._remaining_colours[chosen_colour_name]
                chosen_colour_name, chosen_colour_code = random.choice(list(MemoryRegionImage._remaining_colours.items()))

            # del MemoryRegionImage._remaining_colours[chosen_colour_name]
            logging.debug(f"\tSelected {chosen_colour_name}({chosen_colour_code})")
        except (IndexError, KeyError):
            logging.critical("Ran out of colours!")
            raise SystemExit()
        logging.debug(f"\t### {len(MemoryRegionImage._remaining_colours)} colours left ###")
        return chosen_colour_name

@typeguard.typechecked
class MemoryRegionImage(RegionImage):
    def __str__(self):
        return (
            "|"
            + "<span style='color:"
            + str(self.colour)
            + "'>"
            + str(self.name)
            + "</span>|"
            + str(self.origin_as_hex)
            + "|"
            + str(self.size_as_hex)
            + "|"
            + str(self.freespace_as_hex)
            + "|"
            + str(self.collisions)
            + "|"
        )

    def get_data_as_list(self) -> List:
        """Get selected instance attributes"""
        if self.collisions:
            return [
                str(self.name),
                str(self.origin_as_hex),
                str(self.size_as_hex),
                str(self.freespace_as_hex),
                "-" + str(self.collisions),
            ]
        else:
            return [
                str(self.name),
                str(self.origin_as_hex),
                str(self.size_as_hex),
                str(self.freespace_as_hex),
                "+" + str(None),
            ]

    def create_img(self, img_width: int, font_size: int):

        logging.info(self)
        if not self.size_as_hex:
            logging.warning("Zero size region will not be added.")
            return None

        # MemoryRegionImage Blocks and text
        region_img = PIL.Image.new("RGBA", (img_width, int(self.size_as_hex,16)), color="white")
        self.region_canvas = PIL.ImageDraw.Draw(region_img)

        # height is -1 to avoid clipping the top border
        self.region_canvas.rectangle(
            (0, 0, img_width, int(self.size_as_hex,16) - 1),
            fill=self.colour,
            outline=self.bordercolour,
            width=1,
        )

        # draw name text
        region_img.paste(TextLabelImage(text=self.name, font_size=font_size).img, (5, 5))

        self.img = region_img

@typeguard.typechecked
class VoidRegionImage():

    def __init__(self):

        self.name: str = "~~~~~ SKIPPED ~~~~~"
        self.img: PIL.Image = None
        self.size_as_hex: str = 40

        # super().__init__("None", self.name, "0x0", size)

    def create_img(self, img_width: int, font_size: int):

        logging.info(self)

        # MemoryRegionImage Blocks and text
        self.img = PIL.Image.new("RGBA", (img_width + 1, self.size_as_hex), color="white")
        self.region_canvas = PIL.ImageDraw.Draw(self.img)

        # height is -1 to avoid clipping the top border
        self.region_canvas.rectangle(
            (0, 0, img_width, self.size_as_hex - 1),
            fill="oldlace",
            outline="black",
            width=1,
        )

        # draw name text
        region_w, region_h = self.img.size
        txt_img = TextLabelImage(text=self.name, font_size=font_size).img
        self.img.paste(
            txt_img,
            ((img_width - txt_img.width) // 2, (self.size_as_hex - txt_img.height) // 2),
        )


@typeguard.typechecked
class TextLabelImage:
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

        self.img: PIL.Image.Image
        """The image object. Use this with PIL.Image.paste()"""

        self._create_img()

    def _create_img(self):

        # make the image bigger than the actual text bbox so there is plenty of space for the text
        self.img = PIL.Image.new("RGB", (self.width * 2, self.height * 2), color=self.bgcolour)
        canvas = PIL.ImageDraw.Draw(self.img)
        # center the text in the oversized image, bias the y-pos by 1/5
        canvas.text(
            xy=(self.width / 2, (self.height / 2 - (self.height / 5))),
            text=self.text,
            fill=self.fgcolour,
            font=self.font,
        )

        # the final diagram image will be flipped so start with the text upside down
        self.img = self.img.rotate(180)


class Table:

    def _position_tuple(self, *args):
        from collections import namedtuple

        Position = namedtuple("Position", ["top", "right", "bottom", "left"])
        if len(args) == 0:
            return Position(0, 0, 0, 0)
        elif len(args) == 1:
            return Position(args[0], args[0], args[0], args[0])
        elif len(args) == 2:
            return Position(args[0], args[1], args[0], args[1])
        elif len(args) == 3:
            return Position(args[0], args[1], args[2], args[1])
        else:
            return Position(args[0], args[1], args[2], args[3])

    def draw_table(
        self,
        table,
        header=[],
        font=PIL.ImageFont.load_default(),
        cell_pad=(20, 10),
        margin=(10, 10),
        align=None,
        colors={},
        stock=False,
    ) -> PIL.Image:
        """
        Draw a table using only Pillow
        table:    a 2d list, must be str
        header:   turple or list, must be str
        font:     an ImageFont object
        cell_pad: padding for cell, (top_bottom, left_right)
        margin:   margin for table, css-like shorthand
        align:    None or list, 'l'/'c'/'r' for left/center/right, length must be the max count of columns
        colors:   dict, as follows
        stock:    bool, set red/green font color for cells start with +/-
        """
        _color = {
            "bg": "white",
            "cell_bg": "white",
            "header_bg": "gray",
            "font": "black",
            "rowline": "black",
            "colline": "black",
            "red": "red",
            "green": "green",
        }
        _color.update(colors)
        _margin = self._position_tuple(*margin)

        table = table.copy()
        if header:
            table.insert(0, header)
        row_max_hei = [0] * len(table)
        col_max_wid = [0] * len(max(table, key=len))
        for i in range(len(table)):
            for j in range(len(table[i])):
                left, top, right, bottom = font.getbbox(table[i][j])
                col_max_wid[j] = max(right - left, col_max_wid[j])
                row_max_hei[i] = max(bottom - top, row_max_hei[i])
        tab_width = sum(col_max_wid) + len(col_max_wid) * 2 * cell_pad[0]
        tab_heigh = sum(row_max_hei) + len(row_max_hei) * 2 * cell_pad[1]

        tab = PIL.Image.new(
            "RGBA",
            (
                tab_width + _margin.left + _margin.right,
                tab_heigh + _margin.top + _margin.bottom,
            ),
            _color["bg"],
        )
        draw = PIL.ImageDraw.Draw(tab)

        draw.rectangle(
            [
                (_margin.left, _margin.top),
                (_margin.left + tab_width, _margin.top + tab_heigh),
            ],
            fill=_color["cell_bg"],
            width=0,
        )
        if header:
            draw.rectangle(
                [
                    (_margin.left, _margin.top),
                    (
                        _margin.left + tab_width,
                        _margin.top + row_max_hei[0] + cell_pad[1] * 2,
                    ),
                ],
                fill=_color["header_bg"],
                width=0,
            )

        top = _margin.top
        for row_h in row_max_hei:
            draw.line(
                [(_margin.left, top), (tab_width + _margin.left, top)],
                fill=_color["rowline"],
            )
            top += row_h + cell_pad[1] * 2
        draw.line(
            [(_margin.left, top), (tab_width + _margin.left, top)],
            fill=_color["rowline"],
        )

        left = _margin.left
        for col_w in col_max_wid:
            draw.line(
                [(left, _margin.top), (left, tab_heigh + _margin.top)],
                fill=_color["colline"],
            )
            left += col_w + cell_pad[0] * 2
        draw.line(
            [(left, _margin.top), (left, tab_heigh + _margin.top)],
            fill=_color["colline"],
        )

        top, left = _margin.top + cell_pad[1], 0
        for i in range(len(table)):
            left = _margin.left + cell_pad[0]
            for j in range(len(table[i])):
                color = _color["font"]
                if stock:
                    if table[i][j].startswith("+"):
                        color = _color["red"]
                    elif table[i][j].startswith("-"):
                        color = _color["green"]
                _left = left
                if (align and align[j] == "c") or (header and i == 0):
                    _left += (col_max_wid[j] - font.getlength(table[i][j])) // 2
                elif align and align[j] == "r":
                    _left += col_max_wid[j] - font.getlength(table[i][j])
                draw.text((_left, top), table[i][j], font=font, fill=color)
                left += col_max_wid[j] + cell_pad[0] * 2
            top += row_max_hei[i] + cell_pad[1] * 2

        return tab
