import os
import cv2


from os.path import isfile, join
onlyfiles = [f for f in os.listdir("pkmn") if isfile(join("pkmn", f))]

os.makedirs("resized3",exist_ok=True)
os.makedirs("resized3/img_align_pkmn",exist_ok=True)

sizes = {}
for i in onlyfiles:
    # get image 
    image = cv2.imread(join("pkmn", i)) 
    height, width = image.shape[:2] 
    if (height, width) in sizes:
        sizes[(height, width)].append(i)
    else:
        sizes[(height, width)] = [i]
    resized = cv2.resize(image, (200,280), interpolation = cv2.INTER_AREA)

    cv2.imwrite(r"resized3/img_align_pkmn/"+i, resized)
print([(i, len(sizes[i])) for i in sizes])