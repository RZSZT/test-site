from PIL import Image
import os
from glitchportal_app import colourtextimager
from glitchportal_app import showncapture
import glob
        

def crop_center(pil_img, crop_width, crop_height):
        
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                        (img_height - crop_height) // 2,
                        (img_width + crop_width) // 2,
                        (img_height + crop_height) // 2))


def find_duration(img_obj):
    img_obj.seek(0)  # move to the start of the gif, frame 0
    tot_duration = 0
    # run a while loop to loop through the frames
    while True:
        try:
            frame_duration = img_obj.info['duration']  # returns current frame duration in milli sec.
            tot_duration += frame_duration
            # now move to the next frame of the gif
            img_obj.seek(img_obj.tell() + 1)  # image.tell() = current frame
        except EOFError:
            return tot_duration # this will return the tot_duration of the gif


def gifThis(filename):
    
    percentage = 0
    print(filename)
    #filename = input("GIF filename: ")
    # create new folder
    Filename = filename[6:]
    folder_name = 'media' + Filename.split(".")[0]
    print(folder_name)
    
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
        print(folder_name + " CREATED")
    # save percentage to JSON for JavaScript
    #dict = {"percentage": percentage}
    #with open(foldername + "/progress.json", "w") as outfile:
    #    json.dump(dict, outfile)
    
    # process the GIF
    im = Image.open("../glitchportal" + filename)
    # get number of frames
    frames = im.n_frames
    print("Frames: " + str(frames))
    
    # get the gif duration
    gif_duration = find_duration(im)
    
    # create list for temp images and new images
    temp_files = []
    new_images = []

    # create individual ASCII images from each frame
    for f in range(0, frames):
        # get percentage
        percentage = int(((f + 1) / frames) * 100) 
        # grab frame
        im.seek(f)
        # name frame and save in temp_images
        tempName = folder_name + "/frame" + str(f) + ".png"
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
        gifFile = snc.now()
        # add processed filename to list
        new_images.append(Image.open(gifFile)) #snc.now())
        # save percentage to JSON
        #dict = {"percentage": percentage}
        #with open(foldername + "/progress.json", "w") as outfile:
        #    json.dump(dict, outfile)
        
    # create a new GIF with the ASCII images
    editFilename = filename.replace("/media", "")
    newFilename = folder_name + editFilename
    newFilename = newFilename.replace("_uploads/", "_")
    new_images[0].save(newFilename, save_all=True, append_images=new_images[1:], optimize=False, duration=100, loop=0)
    
    # add one in the static directory
    new_images[0].save("glitchportal_app/static" + editFilename, save_all=True, append_images=new_images[1:], optimize=False, duration=100, loop=0)
    
    # remove the original frame image from temp
    im.close()
    for item in glob.glob(folder_name + "/*.png"):
        #if item[-2:] != "eg":
        os.remove(item)
    
    return newFilename
