# Writen by Alex Eckardt 2023
from PIL import Image
import image_aux
import os

# Contants; Configure
tileSize = 16;
topTile = (1, 0)
leftTile = (0, 1)
rightTile = (2, 1)
bottomTile = (1, 2)

inputdir = "./inputs"
outputdir = "./output"

#
# Show All Files Availaible in in
#
def print_infiles():
    #Setup
    dir_list = os.listdir(inputdir)
    dir_list = [x for x in dir_list if ".png" in x]

    print("\n\nSelect From Input Files in " + inputdir);

    for suitablefile in dir_list:
        suitFileName=suitablefile.replace(".png", "") + " "
        print(suitFileName);


#
# Function To Get Input. LOads File if pass, retrys if fails.
#
def get_input_file():

    print_infiles()

    filename = input("\nEnter Input Cross File Name: ");   

    #Try Getting
    try:
        #Generate Source From Input
        sourceImage = Image.open("{}/{}.png".format(inputdir, filename));
        return filename, sourceImage
    except:
        print("\n\nNo PNG file with that name exists in {}".format(inputdir))
        return None, None

#
#
def start_process():

     #Input
    filename = None;
    sourceImage = None;

    #
    while (sourceImage == None):
        filename, sourceImage = get_input_file();

    #Generate Set
    generate_set(filename, sourceImage);


def generate_set(fileName, sourceImage):

    #Get Source Dimentions
    width, height = sourceImage.size;

    #
    #Check Dimentions Are Good.
    threetiles = tileSize*3;
    if (width != threetiles):
        raise Exception("Width Of Source Image Dimention should be " + str(threetiles) + " pixels long. " + 
                            "Currently is " + str(width) + " pixels wide.")

    if (height != threetiles):
        raise Exception("Height Of Source Image Dimention should be " + str(threetiles) + " pixels long. " + 
                        "Currently is " + str(height) + " pixels high.")

    #
    #Generate Temp Image
    finalImage = Image.new('RGBA', (tileSize*7, tileSize*6))

    #
    #
    #   GENERATING TILE IMAGES
    #
    #  

    #
    #Create Edge Sprites
    #

    #Prep For Placement
    image_aux.cloneTile(sourceImage, finalImage, topTile, (0, 0));
    image_aux.cloneTile(sourceImage, finalImage, topTile, (2, 0));
    image_aux.cloneTile(sourceImage, finalImage, leftTile, (0, 2));
    image_aux.cloneTile(sourceImage, finalImage, rightTile, (2, 2));

    #Clone Tops
    image_aux.cloneTileBottomLeftHalf(sourceImage, finalImage, leftTile, (0, 0));
    image_aux.cloneTileBottomRightHalf(sourceImage, finalImage, rightTile, (2, 0));
    #Clone Bottoms
    image_aux.cloneTileBottomLeftHalf(sourceImage, finalImage, bottomTile, (2, 2));
    image_aux.cloneTileBottomRightHalf(sourceImage, finalImage, bottomTile, (0, 2));

    #
    #Create Inverse Edge Tiles
    #

    #
    #Position For Placement
    image_aux.cloneTile(sourceImage, finalImage, bottomTile, (3, 0));
    image_aux.cloneTile(sourceImage, finalImage, bottomTile, (4, 0));
    image_aux.cloneTile(sourceImage, finalImage, rightTile, (3, 1));
    image_aux.cloneTile(sourceImage, finalImage, leftTile, (4, 1));

    #Clone Tops
    image_aux.cloneTileBottomLeftHalf(sourceImage, finalImage, rightTile, (3, 0));
    image_aux.cloneTileBottomRightHalf(sourceImage, finalImage, leftTile, (4, 0));
    #Clone Bottoms
    image_aux.cloneTileBottomLeftHalf(sourceImage, finalImage, topTile, (4, 1));
    image_aux.cloneTileBottomRightHalf(sourceImage, finalImage, topTile, (3, 1));

    #
    # Create Ramps

    #
    #Create Input Images
    sourceRampImageTop = Image.new('RGBA', (tileSize, tileSize))
    sourceRampImageBottom = Image.new('RGBA', (tileSize, tileSize))
    image_aux.cloneTile(sourceImage, sourceRampImageTop, topTile, (0, 0));
    image_aux.cloneTile(sourceImage, sourceRampImageBottom, bottomTile, (0, 0));

    #Create 2 Long Top Ramp, Clone to Final Image
    rampA, rampB = image_aux.generate_top_ramp(sourceRampImageTop, 2);
    image_aux.cloneImage(rampA, finalImage, 5*tileSize, 0*tileSize)
    image_aux.cloneImage(rampB, finalImage, 5*tileSize, 2*tileSize)
    rampA.close();
    rampB.close();


    #Create 1 Long Top Ramp, Clone to Final Image
    rampA, rampB = image_aux.generate_top_ramp(sourceRampImageTop, 1);
    image_aux.cloneImage(rampA, finalImage, 3*tileSize, 2*tileSize)
    image_aux.cloneImage(rampB, finalImage, 4*tileSize, 2*tileSize)
    rampA.close();
    rampB.close();

    #Create 2 Long Bottom Ramp, Clone to Final Image
    rampA, rampB = image_aux.generate_bottom_ramp(sourceRampImageBottom, 2);
    image_aux.cloneImage(rampA, finalImage, 3*tileSize, 4*tileSize)
    image_aux.cloneImage(rampB, finalImage, 5*tileSize, 4*tileSize)
    rampA.close();
    rampB.close();

    #Create 1 Long Bottom Ramp, Clone to Final Image
    rampA, rampB = image_aux.generate_bottom_ramp(sourceRampImageBottom, 1);
    image_aux.cloneImage(rampA, finalImage, 1*tileSize, 3*tileSize)
    image_aux.cloneImage(rampB, finalImage, 2*tileSize, 3*tileSize)
    rampA.close();
    rampB.close();

    #
    #
    # SAVING
    #
    #

    #modifySurface.save("test.png");

    #Clone Source Cross To Final (Override any Weirdness if that be)
    image_aux.cloneTile(sourceImage, finalImage, topTile, topTile);
    image_aux.cloneTile(sourceImage, finalImage, leftTile, leftTile);
    image_aux.cloneTile(sourceImage, finalImage, rightTile, rightTile);
    image_aux.cloneTile(sourceImage, finalImage, bottomTile, bottomTile);
    image_aux.cloneTile(sourceImage, finalImage, (1,1), (1,1));

    #Save
    outfilename = "{}/{}.png".format(outputdir, fileName);
    finalImage.save(outfilename);
    print("\nSaved file to " + outfilename + "\n");
    #
    #
    #

    #Close Images
    sourceImage.close();
    finalImage.close();
    sourceRampImageTop.close();
    sourceRampImageBottom.close();