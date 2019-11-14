import subprocess
from PIL import Image
import os
import subprocess
from time import time

def reduce_image(image_path):
    basewidth = 200
    file = image_path
    img = Image.open(file)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(file, optimize=True, quality=95)
    subprocess.call(['chmod', '666', file])
    print("success image resize")
    return "successfuly resize image"
