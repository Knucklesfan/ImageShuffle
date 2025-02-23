import sys
from PIL import Image
import random
import os
def chopsort(item):
    return (item[0]&3)|(item[1]&3)<<2|(item[2]&3)<<4
def chopsortv2(item):
    # return (item[0]&7)|(item[1]&3)<<2|(item[2]&3)<<4 # this produces a very interested effect
    return (item[0]&7)|(item[1]&3)<<3|(item[2]&3)<<5

def mix(x,y,a):
    return x*(1-a)+y*a

if len(sys.argv) > 1:
    if not os.path.exists("frames/"):
        os.makedirs("frames/")
    randsample = False
    try:
        iters = int(sys.argv[2])
        if len(sys.argv) > 4:
            if sys.argv[5] == "frame":
                iters = int(sys.argv[2])
            elif sys.argv[5] == "sample":
                iters = 1
            elif sys.argv[5] == "randsample":
                iters = 1
                randsample = True

        with Image.open(sys.argv[1]).convert('RGBA') as im:
            sortlamb = lambda item:(item[0]+item[1]+item[2])/3
            if(len(sys.argv) > 3):

                if(sys.argv[4] == "r"):
                    sortlamb = lambda item:(item[0])
                if(sys.argv[4] == "g"):
                    sortlamb = lambda item:(item[1])
                if(sys.argv[4] == "b"):
                    sortlamb = lambda item:(item[2])
                if(sys.argv[4] == "sat"):
                    sortlamb = lambda item:(item[0]+item[1]+item[2])/3
            if(sys.argv[3] == "horz"):
                for b in range(0,int(iters)):
                    px = im.load()
                    for i in range(0,im.height):
                        samples = random.randint(1, ((b*b+1)%im.width//2)+1)
                        if b >= int(iters)-1:
                            samples = im.width
                        if iters == 1:
                            samples = int(sys.argv[2])
                        if randsample:
                            samples = random.randint(1, int(sys.argv[2]))

                        offset = 0
                        lastoffset = 0
                        for x in range(0,im.width//samples):
                            rowarr = [px[offset,i]]*samples
                            for y in range(0,samples):
                                rowarr[y] = px[offset,i]
                                offset += 1

                            rowarr.sort(key=sortlamb)
                            for y in range(0,samples):
                                if lastoffset+y < im.width:
                                    px[lastoffset+y,i] = rowarr[y]
                            lastoffset = offset
                    im.save("frames/frame"+str(b)+".png")
            elif(sys.argv[3] == "vert"):
                for b in range(0,int(iters)):
                    px = im.load()
                    for i in range(0,im.width):
                        samples = random.randint(1, ((b*b+1)%im.height//2)+1)
                        if b >= int(iters)-1:
                            samples = im.height
                        if iters == 1:
                            samples = int(sys.argv[2])
                        if randsample:
                            samples = random.randint(1, int(sys.argv[2]))

                        offset = 0
                        lastoffset = 0
                        for x in range(0,im.height//samples):
                            rowarr = [(255,0,0)]*samples
                            for y in range(0,samples):
                                rowarr[y] = px[i,offset]
                                offset += 1

                            rowarr.sort(key=sortlamb)
                            for y in range(0,samples):
                                if lastoffset+y < im.height:
                                    px[i,lastoffset+y] = rowarr[y]
                            lastoffset = offset
                    im.save("frames/frame"+str(b)+".png")
            elif(sys.argv[3] == "both"):
                for b in range(0,int(iters)):
                    px = im.load()
                    for i in range(0,im.width):
                        samples = random.randint(1, ((b*b+1)%im.height//2)+1)
                        if b >= int(iters)-1:
                            samples = im.height
                        if iters == 1:
                            samples = int(sys.argv[2])
                        if randsample:
                            samples = random.randint(1, (int(sys.argv[2])))
                        offset = 0
                        lastoffset = 0
                        for x in range(0,im.height//samples):
                            rowarr = [px[i,offset]]*samples
                            for y in range(0,samples):
                                rowarr[y] = px[i,offset]
                                offset += 1

                            rowarr.sort()
                            for y in range(0,samples):
                                if lastoffset+y < im.height:
                                    px[i,lastoffset+y] = rowarr[y]
                            lastoffset = offset

                        samples = random.randint(1, ((b*b+1)%im.height//2)+1)
                        if b >= int(iters)-1:
                            samples = im.height
                        if iters == 1:
                            samples = int(sys.argv[2])
                        if randsample:
                            samples = random.randint(1, (int(sys.argv[2])))

                        yoffset = 0
                        lastyoffset = 0
                        for x in range(0,im.width//samples):
                            rowarr = [px[yoffset,i]]*samples
                            for y in range(0,samples):
                                rowarr[y] = px[yoffset,i]
                                yoffset += 1

                            rowarr.sort(key=sortlamb)
                            for y in range(0,samples):
                                if lastyoffset+y < im.width:
                                    px[lastyoffset+y,i] = rowarr[y]
                            lastyoffset = yoffset

                    im.save("frames/frame"+str(b)+".png")
            elif(sys.argv[3] == "dechop"):
                for b in range(0,int(iters)):
                    im = Image.open(sys.argv[1]).convert('RGBA'); # we have to reload the image each time because that data gets nuked otherwise?
                    px = im.load()

                    for i in range(0,im.width):
                        samples = random.randint(int(((b/int(sys.argv[2])*2)*im.height)//2)+1, int((b*2/int(sys.argv[2]))*im.height)+2)
                        if b >= int(iters)-1 or samples > im.height:
                            samples = im.height
                        if iters == 1:
                            samples = int(sys.argv[2])
                        if randsample:
                            samples = random.randint(1, int(sys.argv[2]))
                        offset = 0
                        lastoffset = 0
                        for x in range(0,im.height//samples):
                            rowarr = [(255,0,0)]*samples
                            for y in range(0,samples):
                                rowarr[y] = px[i,offset]
                                offset += 1
                            rowarr.sort(key=chopsort)
                            for y in range(0,samples):
                                if lastoffset+y < im.height:
                                    color = [rowarr[y][0]&0xE0,rowarr[y][1]&0xE0,rowarr[y][2]&0xE0,255]
                                    othercolor = ((rowarr[y][0]&0x1C)<<3,(rowarr[y][1]&0x1C)<<3,(rowarr[y][2]&0x1C)<<3,255)
                                    color[0] = int(mix(color[0],othercolor[0],b/int(sys.argv[2])))
                                    color[1] = int(mix(color[1],othercolor[1],b/int(sys.argv[2])))
                                    color[2] = int(mix(color[2],othercolor[2],b/int(sys.argv[2])))

                                    px[i,lastoffset+y] = tuple(color)
                            lastoffset = offset
                    im.save("frames/frame"+str(b)+".png")
            elif(sys.argv[3] == "dechopv2"):
                for b in range(0,int(iters)):
                    im = Image.open(sys.argv[1]).convert('RGBA'); # we have to reload the image each time because that data gets nuked otherwise?
                    px = im.load()

                    for i in range(0,im.width):
                        samples = random.randint(int(((b/int(sys.argv[2])*2)*im.height)//2)+1, int((b*2/int(sys.argv[2]))*im.height)+2)
                        if b >= int(iters)-1 or samples > im.height:
                            samples = im.height
                        if iters == 1:
                            samples = int(sys.argv[2])
                        if randsample:
                            samples = random.randint(1, int(sys.argv[2]))
                        offset = 0
                        lastoffset = 0
                        for x in range(0,im.height//samples):
                            rowarr = [(255,0,0)]*samples
                            for y in range(0,samples):
                                rowarr[y] = px[i,offset]
                                offset += 1
                            rowarr.sort(key=chopsort)
                            for y in range(0,samples):
                                if lastoffset+y < im.height:
                                    color = [rowarr[y][0]&0xE0,rowarr[y][1]&0xE0,rowarr[y][2]&0xE0,255]
                                    othercolor = ((rowarr[y][0]&0x18)<<3,(rowarr[y][1]&0x1C)<<3,(rowarr[y][2]&0x1C)<<3,255)
                                    color[0] = int(mix(color[0],othercolor[0],b/int(sys.argv[2])))
                                    color[1] = int(mix(color[1],othercolor[1],b/int(sys.argv[2])))
                                    color[2] = int(mix(color[2],othercolor[2],b/int(sys.argv[2])))

                                    px[i,lastoffset+y] = tuple(color)
                            lastoffset = offset
                    im.save("frames/frame"+str(b)+".png")

    except OSError:
        pass
else:
    print("python sort.py <filename> <samples/frames> <mode> <sort> <type>")
    print("\t* Filename - self-explanatory")
    print("\t* Samples/Frames - number of frames to generate, or the max width of a sample")
    print("\t* Mode - The sort direction, can be \"horz\",\"vert\",\"both\"")
    print("\t* Sort - The color/attribute to sort by, can be \"r\",\"g\",\"b\",\"sat\"")
    print("\t* Type - The type of sort to perform, can be \"frame\",\"sample\",\"randsample\"")
    print("Frame generates a number of frames for the number put in as the number of frames, and sample generates one frame with a given number of samples")
    print("All images are output to a directory called \"frames\" in the current working directory, that will be created if it doesn't exist.")
    print("Example syntax:")
    print("python sort.py cooper.jpg 100 vert sat randsample")
    print("\t* Creates a random sampled, vertically saturation sorted image from cooper.jpg, with max sample size of 100")
    print("python sort.py cooper.jpg 50 horz r sample")
    print("\t* Creates a static sampled, horizontal red sorted image from cooper.jpg, with sample size of 50")
    print("python sort.py cooper.jpg 100 horz r frame")
    print("\t* Creates a 100 frame horizontal red sorted animation from cooper.jpg")

