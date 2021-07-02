import numpy as np
import matplotlib.pyplot as plt
import cv2 
import pytesseract
import requests,json
import xmltodict
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cp_hc = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Create function to retrieve only the car plate region itself

def carplate_extract(image):
    cp_img= []
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    carplate_rects = cp_hc.detectMultiScale(image,scaleFactor=1.1, minNeighbors=5)
    for x,y,w,h in carplate_rects: 
        cp_img.append(image[y+15:y+h-10 ,x+15:x+w-20]) # Adjusted to extract specific region of interest i.e. car license plate
    return cp_img
def enlarge_img(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)    
    return resized_image
def gvi(plate_number):
    r = requests.get("http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={0}&username=astirick".format(str(plate_number)))
    data = xmltodict.parse(r.content)
    jdata = json.dumps(data)
    df = json.loads(jdata)
    df1 = json.loads(df['Vehicle']['vehicleJson'])
    return df1

def grysc(img):
  carplate = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  carplate = cv2.medianBlur(carplate,3)
  return carplate
def makup(image):
   # Display extracted car license plate image
   carplate_extract_img = carplate_extract(image)
   for i in range(len(carplate_extract_img)):
        carplate_extract_img[i] = grysc(enlarge_img(carplate_extract_img[i], 150))
   return carplate_extract_img

def get_num(img):
  img = makup(img)
  as1 = []
  for j in range(3,14):
     for i in range(len(img)):
        as1.append(pytesseract.image_to_string(img[i],config = f'--psm {j} --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
  return as1

