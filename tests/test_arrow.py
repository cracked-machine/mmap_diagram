import PIL.ImageDraw
import PIL.Image
import mm.image
import pytest
import unittest
import random

# Note: these are unit tests that require visual inspection of the images produced in out/tmp/arrow_X.png
# The arrow block graphic should line up with the expected line+dot vector

p_tail_width = 25
p_head_width = 40

def test_arrow_0():

    src = mm.image.Point(50, 50)
    dst = mm.image.Point(100, 50)    

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)    
    c.text((10,10), text=str(a.degs), fill="black")
    
    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_0.png")

    expected_coords = mm.image.Point(50,31)
    assert expected_coords == actual_coords
    assert a.l == 50

def test_arrow_pos45():

    src = mm.image.Point(50, 50)
    dst = mm.image.Point(100, 100)    

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)    
    c.text((10,10), text=str(a.degs), fill="black")
    

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos45.png")

    expected_coords = mm.image.Point(49,49)
    assert expected_coords == actual_coords
    assert a.l == 70


def test_arrow_pos90():

    src = mm.image.Point(50, 40)
    dst = mm.image.Point(50, 100)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos90.png")
    
    expected_coords = mm.image.Point(31,39)
    assert expected_coords == actual_coords
    assert a.l == 60


def test_arrow_pos135():

    src = mm.image.Point(100, 50)
    dst = mm.image.Point(50, 100)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos135.png")

    expected_coords = mm.image.Point(47, 49)
    assert expected_coords == actual_coords
    assert a.l == 70


def test_arrow_pos180():
 
    src = mm.image.Point(100, 50)
    dst = mm.image.Point(20, 50)    
    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos180.png")

    expected_coords = mm.image.Point(22,30)
    assert expected_coords == actual_coords
    assert a.l == 80

def test_arrow_neg135():

    src = mm.image.Point(100, 100)
    dst = mm.image.Point(50, 50)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_neg135.png")

    expected_coords = mm.image.Point(47, 47)
    assert expected_coords == actual_coords
    assert a.l == 70

def test_arrow_neg90():

    src = mm.image.Point(50, 100)
    dst = mm.image.Point(50, 50)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_neg90.png")

    expected_coords = mm.image.Point(30,52)
    assert expected_coords == actual_coords
    assert a.l == 50


def test_arrow_neg45():

    src = mm.image.Point(50, 100)
    dst = mm.image.Point(100, 50) 

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width = p_head_width, 
        tail_len=75, 
        tail_width=p_tail_width,
        fill="red",
        show_outline=True)
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    actual_coords = mm.image.Point(a.pos.x, a.pos.y)
    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_neg45.png")

    expected_coords = mm.image.Point(49,47)
    assert expected_coords == actual_coords
    assert a.l == 70

