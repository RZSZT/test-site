from PIL import Image
import os
from glitchportal_app import colourtextimager
from glitchportal_app import showncapture
import glob
import shutil


def crop_center(pil_img, crop_width, crop_height):
        
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                        (img_height - crop_height) // 2,
                        (img_width + crop_width) // 2,
                        (img_height + crop_height) // 2))

def convertThis(filename):
    
    percentage = 0
    print(filename)
    #filename = input("GIF filename: ")
    # create new folder
    Filename = filename[6:]
    
    nameList = Filename.split(".")
    
    
    folder_name = 'media' + Filename.split(".")[0]
    print(folder_name)
    
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
        print(folder_name + " CREATED")
    
    TheFile = "../glitchportal/" + filename
    theFile = TheFile.replace("//", "/")
    # process the GIF
    im = Image.open(theFile) #.split("/")[-1])
    # get number of frames
    
    
    # create individual ASCII image
        
    # name frame and save in temp_images
    tempName = folder_name + "/" + filename.split("/")[-1] + ".png"
    #im.save(tempName)
    
    # make IMAGE X = Y Square, SAVE in temp_images
    width, height = im.size
    if width >= height:
        thumb_width = height
    else:
        thumb_width = width
    im_thumb = crop_center(im, thumb_width, thumb_width)
    im_thumb.save(tempName) #, quality=95)

    # process image
    cti = colourtextimager.Process(tempName)
    textFileName, colourList = cti.main()
    snc = showncapture.ThisImage(textFileName, colourList) #cti.main())
    processedFile = snc.now()
    
    # create a new GIF with the ASCII images
    editFilename = filename.replace("/media", "")
    
    
    # remove the original frame image from temp
    im.close()
    
    # add one in the static directory
    shutil.copyfile(processedFile, "glitchportal_app/static" + editFilename) 
   
    
    for item in glob.glob(folder_name + "/*.png"):
        #if item[-2:] != "eg":
        os.remove(item)
    
    return editFilename
