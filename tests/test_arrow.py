import PIL.ImageDraw
import PIL.Image
import mm.image
import pytest
import unittest
import random
# Note: these are unit tests that require visual inspection of the images produced in out/tmp/arrowX.png
# The arrow block graphic should line up with the expected line+dot vector

def test_arrow_0():

    src = mm.image.Point(50, 50)
    dst = mm.image.Point(100, 50)    

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)    
    c.text((10,10), text=str(a.degs), fill="black")

    expected_coords = (50,40)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 50

    bg = a.overlay(bg, actual_coords, 128)    
    
    bg.save("out/tmp/arrow_0.png")

def test_arrow_pos45():

    src = mm.image.Point(50, 50)
    dst = mm.image.Point(100, 100)    

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)    
    c.text((10,10), text=str(a.degs), fill="black")
    
    expected_coords = (50,50)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 70

    bg = a.overlay(bg, actual_coords, 128)    
    
    bg.save("out/tmp/arrow_pos45.png")


def test_arrow_pos90():

    src = mm.image.Point(50, 40)
    dst = mm.image.Point(50, 100)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    
    expected_coords = (40,40)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 60

    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos90.png")

def test_arrow_pos135():

    src = mm.image.Point(100, 40)
    dst = mm.image.Point(50, 100)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    expected_coords = (49,40)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 78

    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos135.png")

def test_arrow_pos180():
 
    src = mm.image.Point(100, 50)
    dst = mm.image.Point(22, 50)    
    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    expected_coords = (22,40)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 78

    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_pos180.png")

def test_arrow_neg135():

    src = mm.image.Point(100, 100)
    dst = mm.image.Point(50, 50)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    expected_coords = (49,49)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 70

    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_neg135.png")

def test_arrow_neg90():

    src = mm.image.Point(50, 100)
    dst = mm.image.Point(50, 50)

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")
    
    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    expected_coords = (40,50)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 50

    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_neg90.png")

def test_arrow_neg45():

    src = mm.image.Point(50, 100)
    dst = mm.image.Point(100, 50) 

    a = mm.image.ArrowBlock(
        src=src,
        dst=dst,
        head_width=20, 
        tail_len=75, 
        tail_width=15, 
        fill="red")
        
    bg = PIL.Image.new("RGBA", (150, 150), color="white")

    c = PIL.ImageDraw.Draw(bg)
    c.ellipse([(dst.x - 5, dst.y - 5), (dst.x + 5, dst.y + 5)], fill="black")
    c.line([(src.x, src.y),(dst.x, dst.y)], fill="black", width=2)
    c.text((10,10), text=str(a.degs), fill="black")

    expected_coords = (50,49)
    actual_coords = (a.pos.x, a.pos.y)
    assert expected_coords == actual_coords
    assert a.l == 70

    bg = a.overlay(bg, actual_coords, 128)    
    bg.save("out/tmp/arrow_neg45.png")
