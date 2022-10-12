# Writen by Alex Eckardt 2022
from PIL import Image;

def cloneRegionCondition(src, dest, x1, y1, x2, y2, xdest, ydest, condition):

    pixelRastor = dest.load();

    w = abs(x2 - x1)
    h = abs(y2 - y1)

    for i in range(w):
        for j in range(h):
            if (condition(i, j)):
                pixel = src.getpixel((x1+i, y1+j))
                pixelRastor[xdest+i, ydest+j] = pixel

#No Condition
def cloneRegion(src, dest, x1, y1, x2, y2, xdest, ydest):
    cloneRegionCondition(src, dest, x1, y1, x2, y2, xdest, ydest, lambda i, j : True)

def cloneImage(src, dest, xdest, ydest):
    width, height = src.size;
    cloneRegion(src, dest, 0, 0, width, height, xdest, ydest);

#Clone Tile
def cloneTile(src, dest, srcTilePos, destTilePos, tileWidth = 16):

    i = srcTilePos[0]
    j = srcTilePos[1]
    desti = destTilePos[0]
    destj = destTilePos[1]

    cloneRegion(src, dest, i*tileWidth, j*tileWidth, (i+1)*tileWidth, (j+1)*tileWidth, desti*tileWidth, destj*tileWidth)
    

def cloneTileBottomLeftHalf(src, dest, srcTilePos, destTilePos, tileWidth = 16):
    
    tilei = srcTilePos[0]
    tilej = srcTilePos[1]
    desti = destTilePos[0]
    destj = destTilePos[1]

    x1 = tilei*tileWidth
    y1 = tilej*tileWidth
    xdest = desti*tileWidth
    ydest = destj*tileWidth

    cloneRegionCondition(src, dest, x1, y1, x1+tileWidth, y1+tileWidth, xdest, ydest, lambda i,j : i < j)

def cloneTileBottomRightHalf(src, dest, srcTilePos, destTilePos, tileWidth = 16):
    
    tilei = srcTilePos[0]
    tilej = srcTilePos[1]
    desti = destTilePos[0]
    destj = destTilePos[1]

    x1 = tilei*tileWidth
    y1 = tilej*tileWidth
    xdest = desti*tileWidth
    ydest = destj*tileWidth

    cloneRegionCondition(src, dest, x1, y1, x1+tileWidth, y1+tileWidth, xdest, ydest, lambda i,j : i >= (tileWidth-j))

#
#
#

def clearImage(src):

    pixelRastor = src.load();
    w, h = src.size;

    for i in range(w):
        for j in range(h):
            pixelRastor[i, j] = (0,0,0,0)

#
# Ramps
#

def ramp_set_pixel(IMG, srcpixel, goalX, j, offset, rise, height, bottom, top):
    
    rise = int(rise)
    IMG[goalX, j-offset - rise] = srcpixel;

    if (top):
        if (j == height-1):
            for l in range(rise):
                IMG[goalX, bottom-1-l] = srcpixel;
    else:
        if (j==0):
            for l in range(j-offset-rise):
                IMG[goalX, l] = srcpixel;

#
#
def generate_top_ramp(inimg, tileSlope, top = True):

    width, height = inimg.size
    bottom = height + width;

    imgA = Image.new('RGBA', (width*tileSlope, bottom))
    imgB = Image.new('RGBA', (width*tileSlope, bottom))
    pixA = imgA.load();
    pixB = imgB.load();

    offset = height - bottom

    #STEAL!
    for i in range(width):

        for j in range(height):

            srcpixel = inimg.getpixel((i, j))

            #Loop
            for k in range(tileSlope):

                #If Width is 3, that means that the tile is 48 wide, we have to clone the 16 tile 3 times.
                goalX = i+k*width;

                riseA = goalX / tileSlope
                riseB = width - (goalX / tileSlope)

                ramp_set_pixel(pixA, srcpixel, goalX, j, offset, riseA, height, bottom, top)
                ramp_set_pixel(pixB, srcpixel, goalX, j, offset, riseB, height, bottom, top)

    #Return End
    return (imgA, imgB)

def generate_bottom_ramp(inimg, tileSlope):
    return generate_top_ramp(inimg, tileSlope, False)