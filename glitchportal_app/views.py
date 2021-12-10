from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from glitchportal_app.forms import GifForm
from glitchportal_app.models import GifModel

from glitchportal_app import asciigif
from glitchportal_app import asciiimage

# Create your views here.
def home(request):
    return render(request, "glitchportal_app/home.html")

def ascii_gif(request):
    # uploaded image?
    if request.method == "POST":# and request.FILES['filename']:
            
        #print(request)
        
        upload = request.FILES['filename']
        
        if  upload.name[-4:].lower() == ".gif":    
            # save the file locally
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            
            # throw the GIF through the mechanism
            newFilename = asciigif.gifThis(file_url)
            print(newFilename)
            #filename = newFilename
            fnames = newFilename.split("/")
            filename = fnames[-1]
            
            return render(request, 'glitchportal_app/result.html', {'filename': filename}) 
            
    # landing page
    else:
        return render(request, "glitchportal_app/ascii_gif.html")

def ascii_image(request):
    
    if request.method == "POST":# and request.FILES['filename']:
            
        print(request)
        
        upload = request.FILES['filename']
        
        imageOptions = [".jpg", ".png", ".bmp", "jpeg"]
        
        if  upload.name[-4:].lower() in imageOptions:    
            # save the file locally
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            
            # throw the image through the mechanism
            newFilename = asciiimage.convertThis(file_url)
            print(newFilename)
            #filename = newFilename
            fnames = newFilename.split("/")
            filename = fnames[-1]
            
            return render(request, 'glitchportal_app/result.html', {'filename': filename})
    else:
        return render(request, "glitchportal_app/ascii_image.html")

def about(request):
    return render(request, "glitchportal_app/about.html")








def process(request, file_url):
    
    # throw the GIF through the mechanism
    newFilename = asciigif.gifThis({{ file_url }})
    print(newFilename)
    #filename = newFilename
    fnames = newFilename.split("/")
    filename = fnames[-1]
    # get the folder name
    Filename = filename[6:]
    folder_name = 'media' + Filename.split(".")[0]
    
    return render(request, 'glitchportal_app/result.html', {'filename': filename}) 






def got_gif(request):
    saved = False
   
    if request.method == "POST":
        #Get the posted form
        currentGifForm = GifForm(request.POST, request.FILES)
      
        if GifForm.is_valid():
            gif = GifModel()
            gif.picture = currentGifForm.cleaned_data["picture"]
            gif.save()
            saved = True
    else:
        currentGifForm = GifForm()
    
    return render(request, 'result.html', locals())
