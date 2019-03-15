"""
Character Detection
(Due date: March 8th, 11: 59 P.M.)

The goal of this task is to experiment with template matching techniques. Specifically, the task is to find ALL of
the coordinates where a specific character appears using template matching.

There are 3 sub tasks:
1. Detect character 'a'.
2. Detect character 'b'.
3. Detect character 'c'.

You need to customize your own templates. The templates containing character 'a', 'b' and 'c' should be named as
'a.jpg', 'b.jpg', 'c.jpg' and stored in './data/' folder.

Please complete all the functions that are labelled with '# TODO'. Whem implementing the functions,
comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in utils.py
and the functions you implement in task1.py are of great help.

Hints: You might want to try using the edge detectors to detect edges in both the image and the template image,
and perform template matching using the outputs of edge detectors. Edges preserve shapes and sizes of characters,
which are important for template matching. Edges also eliminate the influence of colors and noises.

Do NOT modify the code provided.
Do NOT use any API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import any library (function, module, etc.).

Student Name: Varsha Ganesh
UBID : 50288433
Email: vganesh2@buffalo.edu
"""


import argparse
import json
import os
import utils
from task1 import *   # you could modify this line

def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img_path", type=str, default="./data/characters.jpg",
        help="path to the image used for character detection (do not change this arg)")
    parser.add_argument(
        "--template_path", type=str, default="./data/a.jpg",
        choices=["./data/a.jpg", "./data/b.jpg", "./data/a.jpg"],
        help="path to the template image")
    parser.add_argument(
        "--result_saving_directory", dest="rs_directory", type=str, default="./results/",
        help="directory to which results are saved (do not change this arg)")
    args = parser.parse_args()
    return args


def detect(img, template):
    """Detect a given character, i.e., the character in the template image.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        coordinates: list (tuple), a list whose elements are coordinates where the character appears.
            format of the tuple: (x (int), y (int)), x and y are integers.
            x: row that the character appears (starts from 0).
            y: column that the character appears (starts from 0).
    """
    # finding edges and magnitude for image using sobel operator
    img_x = detect_edges(img,sobel_x,True)
    img_y = detect_edges(img,sobel_y,True)
    img_mag = normalize(edge_magnitude(img_x,img_y))
    # finding edges and magnitude for Template image using sobel operator
    template_x = detect_edges(template,sobel_x,True)
    template_y = detect_edges(template,sobel_y,True)
    template_mag = normalize(edge_magnitude(template_x,template_y))
    #Finding Template matching using Template match function
    template_match = findmatch(img_mag,template_mag)
    coordinates = getCoordinates(template_match)
    
    # TODO: implement this function.
    #raise NotImplementedError
    return coordinates

def findmatch(img,kernel):
    #similar to convolve
    #subtracts kernel values from image
    # Least difference gives position of template
    kSize = len(kernel) -1
    padSize = (int)(kSize/2)
    img = utils.zero_pad(img,padSize,padSize)
    TemplateMatch = []
    m=0
    n=0
    sum=0
    for i in range(0,len(img)-kSize):
        row = []
        for j in range(0,len(img[0])-kSize):
            m=0 
            for k in range(i,i+len(kernel)):
                for l in range(j,j+len(kernel)):
                    sum = sum + (img[k][l] - kernel[m][n])
                    n=n+1
                n = 0 
                m=m+1
            row.append(sum)
            sum = 0
        TemplateMatch.append(row)
        row = []
    # TODO: implement this function.
    #raise NotImplementedError
    return TemplateMatch

def getCoordinates(template_match):
    #computing coordinates using Template matching
    Coordinates = []
    #min = 100
    #for i in range(0,len(template_match)):
    #    for j in range(0,len(template_match[0])):
            #finding min value
    #       if(min > utils.absolute(template_match[i][j])):
    #           min = utils.absolute(template_match[i][j])
    
    for i in range(0,len(template_match)):
        for j in range(0,len(template_match[0])):
            #finding positions close to min value
            value = utils.absolute(template_match[i][j])
            if((0 < value)&(value < 0.1)):
                    row =[i,j]
                    print(row)
                    Coordinates.append(row)
    return Coordinates


def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()

    img = read_image(args.img_path)
    template = read_image(args.template_path)
    coordinates = detect(img, template)
    template_name = "{}.json".format(os.path.splitext(os.path.split(args.template_path)[1])[0])
    save_results(coordinates, template, template_name, args.rs_directory)


if __name__ == "__main__":
    main()
