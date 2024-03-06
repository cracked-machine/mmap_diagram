import typeguard
import random
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
import PIL.ImageChops
from typing import List, Dict, Tuple
import typing
import logging
import mm.metamodel
import math
import dataclasses


@dataclasses.dataclass
class Point:
    x: float
    y: float
    # convenience functions for PIL
    def ftuple(self) -> Tuple[float,float]:
        return (self.x, self.y)
    def ituple(self) -> Tuple[float,float]:
        return (int(self.x), int(self.y))
    
@typeguard.typechecked
class Image():

    def __init__(self, name: str, parent: str | None):

        self.img: PIL.Image.Image

        self.parent: str = parent
        self.name: str = name
        """region name"""

        self.line = "black"
        """The border colour to use for the region"""

        self.fill = self._pick_random_colour()
        """random colour for region block"""

        self.abs_pos = Point(0,0)
        self.abs_mid_pos = Point(0,0)

    def _draw(self, **kwargs):
        raise NotImplementedError

    def __init_abs_pos_data(self, xy: Point):
        # retain the absolute positional data relative to the map
        self.abs_pos = xy

        if not self.img:
            logging.warn("Cannot access image properties yet, it is still unitialised")
        else:
            self.abs_mid_pos.x = self.abs_pos.x + (self.img.width // 2)
            self.abs_mid_pos.y = self.abs_pos.y + (self.img.height // 2)

    def overlay(self, dest: PIL.Image.Image, xy: Point = Point(0,0), alpha: int = 255) -> PIL.Image.Image:
        """Overlay this image onto the dest image. Return the composite image"""        
        self.__init_abs_pos_data(xy)

        mask_layer = PIL.Image.new('RGBA', dest.size, (0,0,0,0))
        mask_layer.paste(self.img, xy.ituple())
        
        alpha_layer = mask_layer.copy()
        alpha_layer.putalpha(alpha)
        
        mask_layer.paste(alpha_layer, mask_layer)
        
        return PIL.Image.alpha_composite(dest, mask_layer)

    def trim(self):
        bg = PIL.Image.new(self.img.mode, self.img.size, self.img.getpixel((0,0)))
        diff = PIL.ImageChops.difference(self.img, bg)
        diff = PIL.ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            self.img = self.img.crop(bbox) 
        else:
            logging.warning("Error trimming image")
   
    def _pick_random_colour(self):

        r =random.randint(0, int("FF", 16))
        g =random.randint(0, int("FF", 16))
        b =random.randint(0, int("FF", 16))
        a =random.randint(0, int("FF", 16))
        return (r, g, b, a)

@typeguard.typechecked
class MapNameImage(Image):

    def __init__(self, name: str, img_width: int, font_size: int, fill_colour:str, line_colour: str):

        super().__init__(name, None)
        
        self._draw(img_width, font_size, fill_colour, line_colour)

    def _draw(self, img_width: int, font_size: int, fill_colour:str, line_colour: str):
        """Create the image for the region rectangle and its inset name label"""

        txt_lbl =  TextLabelImage(self.name, text=self.name, font_size=font_size)

        generic_img = DashedRectangle(img_width, 
                                      txt_lbl.img.height + 10, 
                                      fill=fill_colour, 
                                      line=line_colour, 
                                      dash=(8,0,8,0), 
                                      stroke=2).img


        # draw name text
        generic_img = txt_lbl.overlay(generic_img, 
                                      mm.image.Point((img_width - txt_lbl.img.width) // 2, 5), 
                                      alpha=192)

        self.img = generic_img

@typeguard.typechecked
class MemoryRegionImage(Image):
    _colour_mappings = {}

    def __init__(self, name: str, mmap_parent: str, metadata: mm.metamodel.MemoryRegion, img_width: int, font_size: int):

        super().__init__(name, mmap_parent)

        self.img = None
        """Pillow image object, initialised by _draw function"""

        self.metadata: mm.metamodel.MemoryRegion = metadata
        """instance of the pydantic metamodel class for this specific memory region"""

        self.draw_indent = 0
        """Index counter for incrementally shrinking the drawing indent"""
        
        self.fill = None
        self._reserve_random_colour()
        
        self.img_width = img_width
        self.font_size = font_size     

    @property
    def origin_as_hex(self):
        """ lookup origin from metamodel  """
        return hex(self.metadata.origin)

    @property
    def size_as_hex(self):
        """ lookup size from metamodel  """
        return hex(self.metadata.size)

    @property
    def freespace_as_hex(self):
        """ lookup memory_region freespace from metamodel  """
        return hex(self.metadata.freespace)

    @property
    def origin_as_int(self):
        """ lookup origin from metamodel  """
        return self.metadata.origin

    @property
    def size_as_int(self):
        """ lookup size from metamodel  """
        return self.metadata.size

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

    def _reserve_random_colour(self):
        r =random.randint(0, int("FF", 16))
        g =random.randint(0, int("FF", 16))
        b =random.randint(0, int("FF", 16))
        a =random.randint(0, int("FF", 16))

        # TODO use parent name to add scope
        if not self.name in MemoryRegionImage._colour_mappings:
            MemoryRegionImage._colour_mappings[self.name] = (r, g, b, a)

        for link in self.metadata.links:
            if not link[1] in MemoryRegionImage._colour_mappings:
                MemoryRegionImage._colour_mappings[link[1]] = (r, g, b, a)

        return (r, g, b, a)
    
    def _draw(self):
        """Create the image for the region rectangle and its inset name label"""

        self.fill = MemoryRegionImage._colour_mappings[self.name]
        logging.info(self)

        if self.freespace_as_int < 0:
            region_img = DashedRectangle(
                self.img_width, int(self.size_as_hex,16), fill=self.fill, line=self.line, dash=(0,0,8,0), stroke=2).img
        else:
            region_img = DashedRectangle(
                self.img_width, int(self.size_as_hex,16), fill=self.fill, line=self.line, dash=(0,0,0,0), stroke=2).img

        # draw name text
        txt_lbl =  TextLabelImage(self.name, text=self.name, font_size=self.font_size, fill_colour="white", padding_width=10)

        region_img = txt_lbl.overlay(region_img, mm.image.Point((self.img_width - txt_lbl.img.width) // 2, 2), alpha=128 )

        self.img = region_img

@typeguard.typechecked
class VoidRegionImage(Image):

    def __init__(self, mmap_parent: str, img_width: int, font_size: int, fill_colour:str, line_colour: str):
        super().__init__("SKIPPED", mmap_parent)
        
        self.size_as_hex: str = hex(40)
        self.size_as_int: int = int(self.size_as_hex,16)
        
        self._draw(img_width, font_size, fill_colour, line_colour)

    def _draw(self, img_width: int, font_size: int, fill_colour:str, line_colour: str):

        logging.info(self)

        self.img = DashedRectangle(img_width, 
                                   self.size_as_int, 
                                   dash=(8,0,8,0), 
                                   stroke=2, 
                                   fill=fill_colour, 
                                   line=line_colour).img

        # draw name text
        txt_img = TextLabelImage(self.name, text=self.name, font_size=font_size, font_colour="grey", fill_colour=fill_colour).img
        self.img.paste(
            txt_img,
            ((img_width - txt_img.width) // 2, (self.size_as_int - txt_img.height) // 2),
        )


@typeguard.typechecked
class TextLabelImage(Image):
    def __init__(self, 
                 parent: str,
                 text: str, 
                 font_size: int, 
                 font_colour: str = "black", 
                 fill_colour: Tuple[int, int, int, int] | str = "white",
                 padding_width: int = 0):
        

        super().__init__(text, parent)

        self.font = PIL.ImageFont.load_default(font_size)
        """The font used to display the text"""

        left, top, right, bottom = self.font.getbbox(self.name)
        """The dimensions required for the text"""

        self.width = right
        """The label width"""

        self.height = bottom
        """The label height"""

        self.bgcolour = fill_colour
        """The background colour to use for the region text label"""

        self.fgcolour = font_colour
        """The foreground colour to use for the region text label"""

        self.padding_width = padding_width
        self._draw()

    def _draw(self):

        # make the image bigger than the actual text bbox so there is plenty of space for the text
        self.img = PIL.Image.new(
            "RGBA", 
            (self.width + self.padding_width, (self.height)), 
            color=self.bgcolour)
        
        canvas = PIL.ImageDraw.Draw(self.img)
        # center the text in the oversized image, bias the y-pos by 1/5
        canvas.text(
            xy=((self.img.width - self.width) // 2, -1),
            text=self.name,
            fill=self.fgcolour,
            font=self.font,
        )

        # the final diagram image will be flipped so start with the text upside down        
        self.img = self.img.transpose(PIL.Image.FLIP_TOP_BOTTOM)

@typeguard.typechecked
class ArrowBlock(Image):
    def __init__(self, 
                 src: Point,
                 dst: Point,
                 head_width: int = 20,
                 tail_len: int = 75, 
                 tail_width: int = 50, 
                 line: str = "black", 
                 fill: str = "white",
                 show_outline: bool = False):
        """
        src: coords for start of arrow
        dst: coords for end of arrow
        head_width: width of the arrow head in pixels
        tail_len: The arrow tail length precentage out of the arrow length total (determined by dst - src). Clamped between 10% and 90%
        tail_width: The arrow tail width precentage out of the arrow head width. Clamped between 10% and 90%
        line: line colour
        fill: fill colour        
        """
        # We need the functions from the base class
        super().__init__("Arrow", None)

        self.l = int(math.hypot((dst.x - src.x), (dst.y - src.y)))
        
        # even numbers are impossible to center...
        if not head_width % 2:
            head_width = head_width - 1

        h = head_width
        max_arrow_head_width = h

        # convert percentages to fraction denominator
        if tail_len <= 10: tail_len = 10
        if tail_len > 90: tail_len = 90
        body_len_dec = (tail_len / 100)
        body_len_denom = 1 / body_len_dec

        if tail_width <= 10: tail_width = 10
        if tail_width > 90: tail_width = 90
        body_width_dec = (tail_width / 100)
        arrow_body_width = max_arrow_head_width * body_width_dec      

        self.midypos = arrow_body_width

        # image needs enough height to rotate the arrow without clipping at top and bottom...
        self.img = PIL.Image.new("RGBA", (self.l, self.l))        
        # and establish relative midpoint for y axis so that arrow is drawn in the center of the image
        yzero = (self.l / 2)  - (h / 2)

        canvas = PIL.ImageDraw.Draw(self.img)
        canvas.polygon(
            [
                (0, yzero + (max_arrow_head_width / 2) - (arrow_body_width / 2)), 
                (self.l//body_len_denom, yzero + (max_arrow_head_width / 2) - (arrow_body_width / 2)), 
                (self.l//body_len_denom, yzero), 
                (self.l, yzero + (max_arrow_head_width / 2)),  # tip of arrow head
                (self.l//body_len_denom, yzero + h), 
                (self.l//body_len_denom, yzero + (max_arrow_head_width / 2) + (arrow_body_width / 2)), 
                (0, yzero + (max_arrow_head_width / 2) + (arrow_body_width / 2))
            ], 
            fill=fill, 
            outline=line, 
            width=2)
        
        # calc the hypot angle from the opp and adj vectors
        self.degs = math.degrees(math.atan2(dst.y - src.y, dst.x - src.x))        
        self.img = self.img.rotate(self.degs)
        self.img = self.img.transpose(PIL.Image.FLIP_TOP_BOTTOM)  
        
        self.trim()
        if show_outline:
            canvas = PIL.ImageDraw.Draw(self.img)
            canvas.rectangle(
                (0, 0, self.img.width, self.img.height), 
                outline="black", width=3)
            

        if self.degs < 100 and self.degs > 80:      # 90 degs
            x = src.x - (self.img.width // 2) + 1
        elif self.degs < -80 and self.degs > -100:   # -90 degs
            x = src.x - (self.img.width // 2)
        elif self.degs < 90 and self.degs > -90:      # -45 degs
            x = src.x + 1
        else:                                       # -135, 135, 180 degs
            if self.degs > 0:
                x = src.x - self.img.width
            else:
                x = src.x - self.img.width
        
        if self.degs < 10 and self.degs > -10:      # 0 degs
            y = src.y - (self.img.height // 2) + 1
        elif self.degs < 190 and self.degs > 170:   # 180 degs
            y = src.y - self.img.height // 2
        elif self.degs > 0:                         # 45 degs
            y = src.y + 1
        else:                                        # -45, -90, -135 deg 
            y = src.y - self.img.height 

        self.pos = Point(
            x=x,
            y=y
        )

        


@typeguard.typechecked
class DashedRectangle(Image):
    def __init__(
            self, 
            w: int, 
            h: int, 
            dash: Tuple[int, int, int, int],
            fill: Tuple[int, int, int, int] | str, 
            line: str = "black", 
            stroke: float = 1):
        """dash is 4-tuple of top, right, bottom, left edges, set to 0 or 1 to disable.
        Fill is an RGBA tuple or colour string"""

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

    def get_table_img(
        self,
        table,
        header=[],
        font=PIL.ImageFont.load_default(),
        cell_pad=(20, 10),
        margin=(10, 10),
        align=None,
        colors={},
        stock=False,
    ) -> PIL.Image.Image:
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
