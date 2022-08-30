import sys, os
import PIL
from PIL import Image, ImageOps

#preloads the images for later use
images = [Image.open(x) for x in ['Pieces/1.png','Pieces/2.png','Pieces/3.png','Pieces/4.png','Pieces/5.png','Pieces/6.png']]

#sets the dimensions for one corner of the Icon
width = images[0].size[0] * 2
height = images[0].size[0] * 2

#sets and creates the hash from user input
user = input("Enter value for icon: ")
value = hash(user)
value = str(value)

#pulls out rotate values
rotate = value[0:4]
hold = 3

#splits hash code between 5 sources
UL = int(value[0:hold])
UR = int(value[hold:hold*2])
BL = int(value[hold*2:hold*3])
BR = int(value[hold*3:hold*4])
COLOR = value[hold*4:]

#makes color tuple to set the pixel values
COLOR = (int(COLOR[0:2]) + 100, int(COLOR[2:4]) + 100, int(COLOR[4:6]) + 100)

#creates varibles for setting pixel values
UpperLeft = []
UpperRight = []
BottomLeft = []
BottomRight = []
Invert = False

#Updates images with new color for combonation later
for item in images[UL %6].getdata():
    if item[0] in list(range(0, 50)):
       UpperLeft.append(COLOR)
    else:
        UpperLeft.append(item)

for item in images[UR %6].getdata():
    if item[0] in list(range(0, 50)):
       UpperRight.append(COLOR)
    else:
        UpperRight.append(item)

for item in images[BL %6].getdata():
    if item[0] in list(range(0, 50)):
       BottomLeft.append(COLOR)
    else:
        BottomLeft.append(item)

for item in images[BR %6].getdata():
    if item[0] in list(range(0, 50)):
       BottomRight.append(COLOR)
    else:
        BottomRight.append(item)

#Places new colored images ontop of previous images
images[UL %6].putdata(UpperLeft)
images[UR %6].putdata(UpperRight)
images[BL %6].putdata(BottomLeft)
images[BR %6].putdata(BottomRight)


#rotates images based on values gathered earlier
if rotate[0] != '-':
    UpperLeft = images[UL %6].rotate(int(rotate[0]) % 4 * 90)
else:
    UpperLeft = images[UL %6]
    Invert = True
UpperRight = images[UR %6].rotate(int(rotate[1]) % 4 * 90)
BottomLeft = images[BL %6].rotate(int(rotate[2]) % 4 * 90)
BottomRight = images[BR %6].rotate(int(rotate[3]) % 4 * 90)


# Makes one corner, which will be replicated
new_im = Image.new('RGB', (width, height))
x_offset = images[0].size[0]
y_offset = images[0].size[1]

new_im.paste(UpperLeft, (0, 0))
new_im.paste(UpperRight, (x_offset, 0))
new_im.paste(BottomRight, (x_offset, y_offset))
new_im.paste(BottomLeft, (0, y_offset))

#would save the corner for testing
# new_im.save("test.png")


# Makes Final Version, by replicating and flipping the one formed corner
Final_im = Image.new('RGB', (width*2, height*2))
x_offset = width
y_offset = height
Final_im.paste(new_im, (0, 0))
Final_im.paste(new_im.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT), (x_offset, 0))
Final_im.paste(new_im.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM), (0, y_offset))
hold = new_im.transpose(method=Image.Transpose.FLIP_LEFT_RIGHT)
Final_im.paste(hold.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM), (x_offset, y_offset))

if os.path.exists("./Icons") == False:
    os.mkdir("./Icons", 0o666)

#inverts the color if the hash was negative
if Invert == True:
    Final_im = ImageOps.invert(Final_im)

#saves then shows the Icon
Final_im.save("Icons/" + user + ".png")
Final_im.show()