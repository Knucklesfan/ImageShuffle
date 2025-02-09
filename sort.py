import sys
from PIL import Image
import random
import os
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
                    im.save("frames/myfile"+str(b)+".png")
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
                    im.save("frames/myfile"+str(b)+".png")
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

