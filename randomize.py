import sys
from PIL import Image
import random
if len(sys.argv) > 1:
    try:
        with Image.open(sys.argv[1]).convert('RGBA') as im:
            hiddenmsg = im.load()
            sortchannel = 0
            shufflechannels = [1,2]
            if len(sys.argv) > 1 and sys.argv[2] != "none":
                surfacemsg = Image.open(sys.argv[2]).convert('RGBA').resize((im.width,im.height)).load()
            if len(sys.argv) > 2:
                #i can probably do this programatically, but thats not fun!
                #besides, this is just a fun script
                if sys.argv[3] == "r":
                    sortchannel = 0
                    shufflechannels = [1,2]
                if sys.argv[3] == "g":
                    sortchannel = 1
                    shufflechannels = [0,2]
                if sys.argv[3] == "b":
                    sortchannel = 2
                    shufflechannels = [0,1]
            for i in range(0,im.width):
                for x in range(0,im.height):
                    tmppxl = [0,0,0,255]
                    tmppxl[shufflechannels[0]] = hiddenmsg[i,x][shufflechannels[0]]
                    tmppxl[shufflechannels[1]] = hiddenmsg[i,x][shufflechannels[1]]
                    tmppxl[sortchannel] = int((x/im.height)*255)
                    hiddenmsg[i,x] = tuple(tmppxl)

            for i in range(0,im.width):
                rowarr = [None]*im.height
                for x in range(0,im.height):
                    rowarr[x] = hiddenmsg[i,x]
                random.shuffle(rowarr)
                for x in range(0,im.height):
                    hiddenmsg[i,x] = rowarr[x]
            if len(sys.argv) > 1 and sys.argv[2] != "none":
                for i in range(0,im.width):
                    for x in range(0,im.height):
                        tmppxl = list(hiddenmsg[i,x])
                        tmppxl[shufflechannels[1]] = surfacemsg[i,x][shufflechannels[1]]
                        hiddenmsg[i,x] = tuple(tmppxl)

            im.save("randomized.png")
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


