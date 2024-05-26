import cv2
import numpy as np
import imutils
import easyocr
import argparse

def detect_numberplate(image_src):
    img = cv2.imread(image_src)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Makes a noise reduction filter
    noise_filter = cv2.bilateralFilter(gray, 20, 100, 100)
    # Finds edges
    edged_image = cv2.Canny(noise_filter, 50, 150, L2gradient =True)

    # Finds contours
    contours,h = cv2.findContours(edged_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)  # Sort contours from big to small

    numberplate = None
    # Loops through contours
    for contour in contours:
        # Finds a rect shape contour with four sides
        approx = cv2.approxPolyDP(contour, 30, True)
        if len(approx) == 4:
            numberplate = approx
            break

    # Applies a mask that makes everything black except for the locations where the numberplate location is found
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [numberplate], 0, 255, -1)
    cv2.bitwise_and(img, img, mask=mask)

    # Cropps the image using the mask so it finds the x1 and y1 where the numberplate starts and x2,y2 is the where it ends.
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = img[x1:x2, y1:y2 - 7]

    # Easy ocr to find the text in image
    reader = easyocr.Reader(['da'],gpu=False)
    result = reader.readtext(cropped_image, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', detail=0)
    
    #If ocr finds more that one text it finds out if the text have a length of 7 and clean up spaces and [] in the words
    text=""
    if len(result)>1:
        for item in result:
            word=item.replace(' ', '')
            if len(word)==7:
                text=word
    else:
        text=result[0].replace(' ', '')
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detect a numberplate from an image')
    parser.add_argument('--image', help='Path to image file(.png/.jpg/.jpeg', required=True)
    args = parser.parse_args()
    numberplate = detect_numberplate(args.image)
    print(numberplate)
