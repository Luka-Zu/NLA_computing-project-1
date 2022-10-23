import cv2
from numpy import asarray
from PIL import Image
import numpy as np


def blend_two_image(alpha, path1, path2, pic_num):
    """
    blends two images into one
    :param alpha: opacity of first image, (1-alpha) is opacity for second image
    :param path1: path for first picture
    :param path2: path for second picture
    :param pic_num: name mark for blended image
    """
    # Load images as matrices
    image1 = Image.open(path1)
    image2 = Image.open(path2)

    # determine the correct dimensions for blended image
    width = min(image1.size[0], image2.size[0])
    height = min(image1.size[1], image2.size[1])

    # resize pictures to correct dimensions if necessary
    if image1.size != (width, height):
        image1 = image1.resize((width, height))
    if image2.size != (width, height):
        image2 = image2.resize((width, height))

    # transform pictures into matrix
    picture_matrix_1 = asarray(image1)
    picture_matrix_2 = asarray(image2)

    blended_image = np.add((np.multiply(picture_matrix_1, 1 - alpha)), (np.multiply(picture_matrix_2, alpha)))
    blended_image = np.asarray(blended_image, dtype="uint8")

    # Converting the numpy array into image
    img = Image.fromarray(blended_image)

    # Saving the image
    img.save(f"blended_images/blended_{pic_num}.jpeg")


def generate_images():
    """
    generates 11 different images for different alphas 0.0, 0.1 ... 1.0
    """
    for i in range(0, 11):
        blend_two_image(i * 0.1, "project-1/autumn.jpeg", "project-1/summer.png", i)


def generate_video():
    """
    generates video out of blended images
    """

    # array to store all the frames of video
    img_array = []
    size = (720, 480)  # default dimensions of video

    # this for loop stores frames into array
    for i in range(0, 11):
        img = cv2.imread(f"blended_images/blended_{i}.jpeg")
        height, width, layers = img.shape
        size = (width, height)
        for _ in range(11):
            # I do that so video will be longer and not just 11 frames
            img_array.append(img)

    out = cv2.VideoWriter('project.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])

    out.release()


generate_images()
generate_video()
