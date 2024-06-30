import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import os
import pytesseract

def change_to_gray(img):
     return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
def detect_edge(gray):
     # filter the image
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
    # detect edge
    edged = cv2.Canny(bfilter, 30, 200)
    return edged
def detect_contours(edged):
    # detect counter
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    return contours
def find_location(contours):
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    return approx,location
def merge_contour(img,gray,location):
    # merge contour with original image 
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    return new_image,mask

def crop_image(mask,gray):
     # crop masked image
    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]   
    return cropped_image
def extract_text_easyoct(cropped_image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    text = result[0][-2]
    return text
def extract_text_teseract(cropped_image):
    custom_config = r'--oem 3 --psm 6'
    result = pytesseract.image_to_string(cropped_image, config=custom_config)
    # need to be tested for different images
    text=result[6:13].strip()
    return text
def maskplate_onorginal_image(text,img,approx):
    # mask plate on original image 
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0), 3)
    new_image=cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    return new_image
def decode_image(img):
     _, buffer = cv2.imencode('.jpeg', img)
     img_str = base64.b64encode(buffer).decode()
     return img_str
def show_image(img):
    plt.imshow(img)
    plt.axis('off')  # Hide the axis
    plt.show()

def plate_identify(image_path):
    img = cv2.imread(image_path)
    if img is None:
     error_message=f"Error: Unable to load image at {image_path}"
     print(error_message)
     return error_message
    else:   
        # chanage image to gray
        gray = change_to_gray(img)
        # detect edge
        edged = detect_edge(gray)
        # detect counter
        contours=detect_contours(edged)
        # find location
        approx,location=find_location(contours)
        # merge contour w   text=result[6:13].strip()ith original image 
        merged_image,mask=merge_contour(img,gray,location)
        # crop masked image
        cropped_image=crop_image(mask,gray)
        # Use Tesseract to extract text with the custom configuration
        text=extract_text_teseract(cropped_image)
        # mask plate on original image 
        new_image=maskplate_onorginal_image(text,img,approx)
        rgb_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
        return rgb_image,edged,cropped_image,merged_image,text
def main():
    relative_path='./static/images/img1.jpg'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, relative_path)
    print(image_path)
    plate_identify(image_path)
main()