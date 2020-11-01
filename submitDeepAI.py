import requests
import glob
import os
import re
import sys, getopt
import wget
import cv2


folder = "/Users/rmvpaeme/Desktop/testColorize/"
files = glob.glob(os.path.join(folder, "DSC*_*.jpg"))

# https://github.com/Devyanshu/image-split-with-overlap
# source

for indiv_files in files:
    path_to_img = indiv_files
    base_name = os.path.splitext(os.path.basename(path_to_img))[0]
    img = cv2.imread(path_to_img)
    img_h, img_w, _ = img.shape
    split_width = 1200
    split_height = 1200

    
    def start_points(size, split_size, overlap=0.10):
        points = [0]
        stride = int(split_size * (1-overlap))
        counter = 1
        while True:
            pt = stride * counter
            if pt + split_size >= size:
                points.append(size - split_size)
                break
            else:
                points.append(pt)
            counter += 1
        return points


    X_points = start_points(img_w, split_width, 0.5)
    Y_points = start_points(img_h, split_height, 0.5)

    count = 0
    name = 'splitted'
    name =  path_to_img.replace('.jpg','')
    frmt = 'jpeg'

    for i in Y_points:
        for j in X_points:
            split = img[i:i+split_height, j:j+split_width]
            cv2.imwrite('{}_{}.{}'.format(name, count, frmt), split)
            count += 1


    image_folder = "/Users/rmvpaeme/Desktop/testColorize/"
    image_files = glob.glob(os.path.join(image_folder, base_name + "_*.jpeg"))

    for file in image_files:
        file_name = os.path.splitext(os.path.basename(file))[0]
        print(file_name)
        r = requests.post(
            "https://api.deepai.org/api/colorizer",
            files={
                'image': open(file, 'rb'),
            },
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        )
        print(r.json())
        wget.download(r.json()['output_url'], out = image_folder)
        os.rename(image_folder + "output.jpg", image_folder + "colorized/" + file_name + "_colorized.jpg")
