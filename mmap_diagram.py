import argparse
import itertools
import PIL.Image
import PIL.ImageDraw
import PIL.ImageColor
import PIL.ImageFont
from typing import List, Dict
import typeguard
import random

class mmap():
    def __init__(self):
        self.h = 500
        self.w = 250
        self.menu_size = 50
        

        self.__create_diagram(self.__process_input())
   

    def __create_diagram(self, data_list: List[Dict]):

        
        # init the main image
        img_main = PIL.Image.new("RGB", (self.w, self.h), color=(255,255,255))
        offset = 0
        for data in data_list:
            

            origin = int(data['origin'], 16)
            size = int(data['size'], 16)
            colorpick = random.choice(list(PIL.ImageColor.colormap))
            print("Origin:" + str(origin) + ",Size:" + str(size) +  " - " + colorpick)
            if not size:
                print("Zero size region skipped")
                continue
            offset = offset + 5
            # pick a colour for current region

            # init the layer
            region_img = PIL.Image.new("RGBA", (self.w - self.menu_size, size), color=(255,255,0, 5))
            region_canvas = PIL.ImageDraw.Draw(region_img)

            # draw the region graphic
            region_canvas.rectangle(
                (0, 0, self.w-1, origin + size), 
                fill=colorpick, 
                outline="black", 
                width=1)
            
            # blend overlay with main image so far
            img_main.paste(region_img, (self.menu_size + offset, origin), region_img)          
            
            # add legend for the region
            text_img = PIL.Image.new("RGB", (30, 10), color=(255,255,0))
            text_canvas = PIL.ImageDraw.Draw(text_img)
            text_canvas.text((0, 0), data['origin'], fill='black')
            text_img = text_img.rotate(180)
            img_main.paste(text_img, (0, origin)) 

        # horizontal flip and write to file
        img_main = img_main.rotate(180)
        img_main.save("out.png")

    @typeguard.typechecked
    def __process_input(self) -> List[Dict]:
        parser = argparse.ArgumentParser()
        parser.add_argument('datapairs', nargs='*')
        self.args = parser.parse_args()
        if len(self.args.datapairs) % 2:
            parser.error('datapairs arg should be pairs of values')

        list_of_data_maps = []
        for pair in self.__batched(self.args.datapairs, 2):
            list_of_data_maps.append({'origin': pair[0], 'size': pair[1]} )

        return list_of_data_maps 

    def __batched(self, iterable, n):
        # batched('ABCDEFG', 3) --> ABC DEF G
        if n < 1:
            raise ValueError('n must be at least one')
        it = iter(iterable)
        while batch := tuple(itertools.islice(it, n)):
            yield batch
        

if __name__ == '__main__':
   mmap()