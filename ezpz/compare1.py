from PIL import Image
from PIL import ImageChops
import base64
import requests



class ImageCompareException(Exception):
    pass

def parser64():
    url= "http://localhost:3000/data"
    resp = requests.get(url)
    data = resp.json()
    xd = data['imagedata'].split(",",1)
    imgdata = base64.b64decode(xd[1])
    filename = 'output.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)
        return 1
def pixel_diff(image_a, image_b):
    if image_a.size != image_b.size:
        raise ImageCompareException(
            "different image sizes, can only compare same size images: A=" + str(image_a.size) + " B=" + str(
                image_b.size))

    if image_a.mode != image_b.mode:
        raise ImageCompareException(
            "different image mode, can only compare same mode images: A=" + str(image_a.mode) + " B=" + str(
                image_b.mode))

    diff = ImageChops.difference(image_a, image_b)
    diff = diff.convert('L')

    return diff

def total_histogram_diff(pixel_diff):
    return sum(i * n for i, n in enumerate(pixel_diff.histogram()))


def image_diff(image_a, image_b):
    histogram_diff = total_histogram_diff(pixel_diff(image_a, image_b))

    return histogram_diff


def is_equal(image_a, image_b, tolerance=0.0):
    return image_diff_percent(image_a, image_b) <= tolerance


def image_diff_percent(image_a, image_b):
    # if paths instead of image instances where passed in
    # load the images

    # don't close images if they were not opened inside our function
    close_a = False
    close_b = False
    if isinstance(image_a, str):
        image_a = Image.open(image_a)
        close_a = True

    if isinstance(image_b, str):
        image_b = Image.open(image_b)
        close_b = True

    try:
        # first determine difference of input images
        input_images_histogram_diff = image_diff(image_a, image_b)

        # to get the worst possible difference use a black and a white image
        # of the same size and diff them

        black_reference_image = Image.new('RGB', image_a.size, (0, 0, 0))
        white_reference_image = Image.new('RGB', image_a.size, (255, 255, 255))

        worst_bw_diff = image_diff(black_reference_image, white_reference_image)
        percentage_histogram_diff = (input_images_histogram_diff / float(worst_bw_diff)) * 100
    finally:
        if close_a:
            image_a.close()
        if close_b:
            image_b.close()
    return percentage_histogram_diff

parser64()
img_a = Image.open("5.jpg")
img_b = Image.open("output.jpg")
print(str(10000-image_diff_percent(img_a,img_b)*1000))

