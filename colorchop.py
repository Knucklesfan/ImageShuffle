import sys
from PIL import Image
import random
def v1encode():
    with Image.open(sys.argv[1]).convert('RGBA') as im:
        hiddenmsg = im.load()
        if len(sys.argv) > 1 and sys.argv[2] != "none":
            surfacemsg = Image.open(sys.argv[2]).convert('RGBA').resize((im.width,im.height)).load()

        for i in range(0,im.width):
            for x in range(0,im.height):
                tmppxl = [0,0,0,255]
                formerpxl = hiddenmsg[i,x] # bits are the first 3 for the front, 3 for the back, then the remaining 6 for the sort.
                greenvalue = int((x/im.height)*63)
                tmppxl[0] = ((hiddenmsg[i,x][0]&0xE0)>>3) | greenvalue&0x3 # used bits: fffbbb00
                tmppxl[1] = ((hiddenmsg[i,x][1]&0xE0)>>3) | (greenvalue>>2)&0x3 # used bits: fffbbb00
                tmppxl[2] = ((hiddenmsg[i,x][2]&0xE0)>>3) | (greenvalue>>4)&0x3 # used bits: fffbbb00

                hiddenmsg[i,x] = tuple(tmppxl)
        for i in range(0,im.width):
            rowarr = [None]*im.height
            for x in range(0,im.height):
                rowarr[x] = hiddenmsg[i,x]
            random.shuffle(rowarr)
            for x in range(0,im.height):
                hiddenmsg[i,x] = rowarr[x]
        for i in range(0,im.width):
            for x in range(0,im.height):
                tmppxl = [0,0,0,255]
                formerpxl = surfacemsg[i,x] # bits are the first 3 for the front, 3 for the back, then the remaining 6 for the sort.
                currpxl = hiddenmsg[i,x]
                greenvalue = int((x/im.height)*63)
                tmppxl[0] = (formerpxl[0]&0xE0) + currpxl[0] # used bits: fffbbb00
                tmppxl[1] = (formerpxl[1]&0xE0) + currpxl[1] # used bits: fffbbb00
                tmppxl[2] = (formerpxl[2]&0xE0) + currpxl[2] # used bits: fffbbb00

                hiddenmsg[i,x] = tuple(tmppxl)

        im.save("randomized.png")


def v2encode():
    with Image.open(sys.argv[1]).convert('RGBA') as im:
        hiddenmsg = im.load()
        if len(sys.argv) > 1 and sys.argv[2] != "none":
            surfacemsg = Image.open(sys.argv[2]).convert('RGBA').resize((im.width,im.height)).load()

        for i in range(0,im.width):
            for x in range(0,im.height):
                tmppxl = [0,0,0,255]
                formerpxl = hiddenmsg[i,x] # bits are the first 3 for the front, 3 for the back, then the remaining 6 for the sort.
                greenvalue = int((x/im.height)*128)
                tmppxl[0] = ((hiddenmsg[i,x][0]&0xC0)>>3) | greenvalue&0x7 # used bits: fffbbb00
                tmppxl[1] = ((hiddenmsg[i,x][1]&0xE0)>>3) | (greenvalue>>3)&0x3 # used bits: fffbbb00
                tmppxl[2] = ((hiddenmsg[i,x][2]&0xE0)>>3) | (greenvalue>>5)&0x3 # used bits: fffbbb00

                hiddenmsg[i,x] = tuple(tmppxl)
        for i in range(0,im.width):
            rowarr = [None]*im.height
            for x in range(0,im.height):
                rowarr[x] = hiddenmsg[i,x]
            random.shuffle(rowarr)
            for x in range(0,im.height):
                hiddenmsg[i,x] = rowarr[x]
        for i in range(0,im.width):
            for x in range(0,im.height):
                tmppxl = [0,0,0,255]
                formerpxl = surfacemsg[i,x] # bits are the first 3 for the front, 3 for the back, then the remaining 6 for the sort.
                currpxl = hiddenmsg[i,x]
                tmppxl[0] = (formerpxl[0]&0xE0) | currpxl[0] # used bits: fffbbb00
                tmppxl[1] = (formerpxl[1]&0xE0) | currpxl[1] # used bits: fffbbb00
                tmppxl[2] = (formerpxl[2]&0xE0) | currpxl[2] # used bits: fffbbb00

                hiddenmsg[i,x] = tuple(tmppxl)

        im.save("randomized.png")


if len(sys.argv) > 1:
    try:
        if len(sys.argv) > 3:
            if(sys.argv[3] == "v1"):
                v1encode()
            else:
                v2encode()

    except OSError:
        pass
else:
    print("python randomize.py <source> <cover> <rgb>")
    print("\t* Source - source file name to scramble")
    print("\t* Cover - image to use the extra color layer of to hide an image in this one or setting to \"none\" to not use a cover image (case-sensitive)")
    print("\t* rgb - color to use as sorting mask, can be r,g,b")
    print("Examples:")
    print("python randomize.py cooper.jpg bread.jpg b")
    print("\t* generates a scrambled picture of cooper.jpg, with bread.jpg as the cover image, using the blue channel as the sorting channel")
    print("python randomize.py cooper.jpg none r")
    print("\t* generates a scrambled picture of cooper.jpg with red as the sorting channel")


