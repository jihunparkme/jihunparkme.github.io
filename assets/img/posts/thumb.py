import os
from PIL import Image

# Changing the working path
path = input("input working path") + '/'
os.chdir(path)
os.getcwd()

# image size conversion
thumb = input("input thumb name")
if thumb + '.jpg' in os.listdir(path) :
    image = Image.open(thumb + '.jpg')

    placehold_image = image.resize((230, 129))
    thumb_image = image.resize((535, 301))
    thumb2x_image = image.resize((1070, 602))

    placehold_image.save(path + thumb + '_placehold.jpg', quality=95)
    thumb_image.save(path + thumb + '_thumb.jpg', quality=95)
    thumb2x_image.save(path + thumb + '_thumb@2x.jpg', quality=95)

else :
    print('Wrong Thumbnail name. Please check')

