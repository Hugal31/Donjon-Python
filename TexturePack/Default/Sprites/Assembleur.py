from PIL import Image
from os import listdir

image = Image.new("RGB",(len(listdir('Boss'))*32*3, 4*32), 'white')
cpt = 0

for nom in listdir('Boss'):
    for direc in range(4) : 
        for anim in range(3):
            img = Image.open('Boss\\' + str(nom) + '\\' + str(direc) +str(anim) + '.gif')
            image.paste(img, (cpt*32*3 + anim*32, direc*32))
        del img
    cpt += 1
image.save('Boss.png')
