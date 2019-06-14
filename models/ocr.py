from PIL import Image

import numpy
import cv2
import os
import pytesseract


def transcript(file_input):
    # convert the image to a NumPy array and then read it into
    # OpenCV format
    image = numpy.asarray(bytearray(file_input.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = numpy.column_stack(numpy.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle

    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE)

    # load the rotated image and convert it to grayscale
    gray_rotated = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
    gray_rotated = cv2.threshold(
        gray_rotated, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # write the rotated grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "../temp/tmp_{}".format(file_input.name)
    cv2.imwrite(filename, gray_rotated)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename), lang='kaz')
    os.remove(filename)
    return text