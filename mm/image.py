import typeguard
import random
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
from typing import List, Dict, Tuple
import logging
import mm.metamodel

@typeguard.typechecked
class Image():

    _colours: Dict = PIL.ImageColor.colormap.copy()
    """Copy of the PIL colour string map"""

    @classmethod
    def init(cls):
        # remove any duplicate colour values from the dict
        temp = {val: key for key, val in Image._colours.items()}
        Image._colours = {val: key for key, val in temp.items()}       

    def __init__(self, name: str):
        Image.init()

        self.img: PIL.Image.Image

        self.name: str = name
        """region name"""

        self.line = "black"
        """The border colour to use for the region"""

        self.fill = self._pick_available_colour()
        """random colour for region block"""

    def _draw(self, **kwargs):
        raise NotImplementedError

    def overlay(self, dest: PIL.Image.Image, pos: Tuple[int,int] = (0,0), alpha: int = 255) -> PIL.Image.Image:
        """Overlay this image onto the dest image. Return the composite image"""        

        mask_layer = PIL.Image.new('RGBA', dest.size, (0,0,0,0))
        mask_layer.paste(self.img, pos)

        # from PIL.Image import Transform
        # mask_layer = mask_layer.transform(dest.size, Transform.AFFINE, (1, 0.5, -100, 1, 1, -100))
        
        alpha_layer = mask_layer.copy()
        alpha_layer.putalpha(alpha)
        
        mask_layer.paste(alpha_layer, mask_layer)
        
        return PIL.Image.alpha_composite(dest, mask_layer)
    
    def _pick_available_colour(self) -> str:
        """Pick a random colour from the  remove the picked colour from the list so it can't be picked again"""
        try:
            logging.debug(f"{self.name}:")
            # make sure we don't pick a colour that is too bright.
            # A0A0A0 was arbitrarily decided to be "too bright" :)
            chosen_colour_name, chosen_colour_code = random.choice(list(Image._colours.items()))
            while int(chosen_colour_code[1:], 16) > int("A0A0A0", 16):
                logging.debug(f"\tRejected {chosen_colour_name}({chosen_colour_code})")
                # del Image._colours[chosen_colour_name]
                chosen_colour_name, chosen_colour_code = random.choice(list(Image._colours.items()))

            # del Image._colours[chosen_colour_name]
            logging.debug(f"\tSelected {chosen_colour_name}({chosen_colour_code})")
        except (IndexError, KeyError):
            logging.critical("Ran out of colours!")
            raise SystemExit()
        logging.debug(f"\t### {len(Image._colours)} colours left ###")
        return chosen_colour_name

@typeguard.typechecked
class MemoryRegionImage(Image):

    def __init__(self, name: str, metadata: mm.metamodel.MemoryRegion, img_width: int, font_size: int):

        super().__init__(name)

        self.metadata: mm.metamodel.MemoryRegion = metadata
        """instance of the pydantic metamodel class for this specific memory region"""

        self.draw_indent = 0
        """Index counter for incrementally shrinking the drawing indent"""
        
        self._draw(img_width, font_size)

    @property
    def origin_as_hex(self):
        """ lookup memory_region_origin from metamodel  """
        return hex(self.metadata.memory_region_origin)

    @property
    def size_as_hex(self):
        """ lookup memory_region_size from metamodel  """
        return hex(self.metadata.memory_region_size)

    @property
    def freespace_as_hex(self):
        """ lookup memory_region freespace from metamodel  """
        return hex(self.metadata.freespace)

    @property
    def origin_as_int(self):
        """ lookup memory_region_origin from metamodel  """
        return self.metadata.memory_region_origin

    @property
    def size_as_int(self):
        """ lookup memory_region_size from metamodel  """
        return self.metadata.memory_region_size

    @property
    def freespace_as_int(self):
        """ lookup memory_region freespace from metamodel  """
        return self.metadata.freespace

    @property
    def collisions(self):
        """ lookup memory_region collision from metamodel  """
        from mm.diagram import Diagram
        return self.metadata.collisions

    @property
    def collisions_as_hex(self):
        """ lookup memory_region collision from metamodel  """
        from mm.diagram import Diagram
        d = self.metadata.collisions.copy()
        for k, v in d.items(): d[k] = hex(v)
        return d

    def __str__(self):
        return (
            "|"
            + "<span style='color:"
            + str(self.fill)
            + "'>"
            + str(self.name)
            + "</span>|"
            + str(self.origin_as_hex)
            + "|"
            + str(self.size_as_hex)
            + "|"
            + str(self.freespace_as_hex)
            + "|"
            + str(self.collisions_as_hex)
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
                "-" + str(self.collisions_as_hex),
            ]
        else:
            return [
                str(self.name),
                str(self.origin_as_hex),
                str(self.size_as_hex),
                str(self.freespace_as_hex),
                "+" + str(None),
            ]

    def _draw(self, img_width: int, font_size: int):
        """Create the image for the region rectangle and its inset name label"""

        logging.info(self)
        if not self.size_as_hex:
            logging.warning("Zero size region will not be added.")
            return None

        if self.freespace_as_int < 0:
            region_img = DashedRectangle(
                img_width, int(self.size_as_hex,16), fill=self.fill, line=self.line, dash=(0,0,8,0), stroke=2).img
        else:
            region_img = DashedRectangle(
                img_width, int(self.size_as_hex,16), fill=self.fill, line=self.line, dash=(0,0,0,0), stroke=2).img
            

        # draw name text
        txt_lbl =  TextLabelImage(text=self.name, font_size=font_size)
        region_img = txt_lbl.overlay(region_img, ((img_width - txt_lbl.img.width) // 2, 2), 192 )

        self.img = region_img

@typeguard.typechecked
class VoidRegionImage(Image):

    def __init__(self, img_width: int, font_size: int):
        super().__init__(name="~ SKIPPED ~")
        
        self.size_as_hex: str = hex(40)
        self.size_as_int: int = int(self.size_as_hex,16)
        self._draw(img_width, font_size)

    def _draw(self, img_width: int, font_size: int):

        logging.info(self)

        self.img = DashedRectangle(img_width, self.size_as_int, dash=(8,0,8,0), stroke=2, line="grey").img

        # draw name text
        txt_img = TextLabelImage(text=self.name, font_size=font_size, font_colour="grey").img
        self.img.paste(
            txt_img,
            ((img_width - txt_img.width) // 2, (self.size_as_int - txt_img.height) // 2),
        )


@typeguard.typechecked
class TextLabelImage(Image):
    def __init__(self, text: str, font_size: int, font_colour: str = "black"):
        super().__init__(name=text)

        self.font = PIL.ImageFont.load_default(font_size)
        """The font used to display the text"""

        left, top, right, bottom = self.font.getbbox(self.name)
        """The dimensions required for the text"""

        self.width = right
        """The label width"""

        self.height = bottom
        """The label height"""

        self.bgcolour = "oldlace"
        """The background colour to use for the region text label"""

        self.fgcolour = font_colour
        """The foreground colour to use for the region text label"""

        self._draw()

    def _draw(self):

        # make the image bigger than the actual text bbox so there is plenty of space for the text
        self.img = PIL.Image.new(
            "RGBA", 
            (self.width, (self.height)), 
            color=self.bgcolour)
        
        canvas = PIL.ImageDraw.Draw(self.img)
        # center the text in the oversized image, bias the y-pos by 1/5
        canvas.text(
            # xy=(self.width / 2, (self.height / 2 - (self.height / 5))),
            xy=(0, -1),
            text=self.name,
            fill=self.fgcolour,
            font=self.font,
        )

        # the final diagram image will be flipped so start with the text upside down        
        self.img = self.img.transpose(PIL.Image.FLIP_TOP_BOTTOM)

@typeguard.typechecked
class ArrowBlock(Image):
    def __init__(self, size: int = 20, line: str = "black", fill: str = "white"):

        # draw an arrow in the unit square (4px by 4px)
        w = 4 * size
        h = 4 * size

        self.img = PIL.Image.new("RGBA", (w + 1, h + 1))        
        arrow_draw = PIL.ImageDraw.Draw(self.img)
        arrow_draw.polygon(
            [
                (0, h//4), (w//2, h//4), (w//2, 0), (w, h//2),
                (w//2, h), (w//2, h//2 + h//4), (0, h//2 + h//4)
            ], 
            fill=fill, 
            outline=line, 
            width=2)

@typeguard.typechecked
class DashedRectangle(Image):
    def __init__(
            self, 
            w: int, 
            h: int, 
            dash: Tuple[int, int, int, int] = (0,0,0,0),
            fill: str = "white", 
            line: str = "black", 
            stroke: float = 1):
        """dash is 4-tuple of top, right, bottom, left edges, set to 0 or 1 to disable"""

        top_dash = dash[0] if dash[0] > 1 else 1
        
        bottom_dot = dash[2] if dash[2] > 1 else 1
        

        self.img = PIL.Image.new("RGBA", (w , h), color=fill)        
        canvas = PIL.ImageDraw.Draw(self.img)
        line_center = (stroke // 2)  
        
        # start from top edge at 0,0 and go clockwise back to 0,0

        # top line: enable dash with top_dash > 1
        if top_dash > 1:
            for x in range(0, w, top_dash):
                if stroke % 2:
                    canvas.line(xy=[(x, line_center), 
                                    (x + (top_dash // 2), line_center)], 
                                fill=line, width=stroke)
                else:
                    canvas.line(xy=[(x, line_center - 1), 
                                    (x + (top_dash // 2), line_center - 1)], 
                                fill=line, width=stroke)        
        else:
            if stroke % 2:
                canvas.line(xy=[(0, line_center), 
                                (w, line_center)], 
                            fill=line, width=stroke)
            else:
                canvas.line(xy=[(0, line_center - 1), 
                                (w, line_center - 1)], 
                            fill=line, width=stroke)   
        # right line
        canvas.line(xy=[(w - line_center - 1, 0), 
                        (w - line_center - 1, h - line_center - 1)], 
                    fill=line, width=stroke)
        
                                
        # bottom line: enable dash with top_dash > 1
        if bottom_dot > 1:
            for x in range(0, w, bottom_dot):
                canvas.line(xy=[(x, h - line_center - 1), 
                                (x + (bottom_dot // 2), h - line_center - 1)], 
                            fill=line, width=stroke)
        else:
            canvas.line(xy=[(0, h - line_center - 1), 
                            (w, h - line_center - 1)], 
                        fill=line, width=stroke)            

        # left line
        if stroke % 2:
            canvas.line(xy=[(line_center, 0), 
                            (line_center, h - line_center - 1)], 
                        fill=line, width=stroke)
        else:
            canvas.line(xy=[(line_center - 1, 0), 
                            (line_center - 1, h - line_center - 1)], 
                        fill=line, width=stroke)
            


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
