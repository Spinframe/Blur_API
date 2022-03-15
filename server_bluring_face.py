
import os
import json
from flask_cors import cross_origin
from numpy import array, float32
os.environ['MXNET_CUDNN_AUTOTUNE_DEFAULT'] = '0'

import threading
from datetime import datetime


from flask import Flask, flash, request, redirect


import time
from PIL import Image
from PIL import ImageDraw


from google.cloud import vision
import io
import cv2
from os import listdir
from os.path import isfile, join
import base64





UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

#UPLOAD_BASE = 'C:\\spinframe-ai\\uploads\\'
#OUT_BASE = 'C:\\Websites\\spinframe-app\\out\\'
UPLOAD_BASE = 'C:\\Users\\hadas\\Desktop\\spinframe_onWork\\API_function\\blure\\uploads\\'
OUT_BASE = 'C:\\Users\\hadas\\Desktop\\spinframe_onWork\\API_function\\blure\\out_api\\'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

lock = threading.Lock()


def str_to_bool(str):
    if str.lower() == 'true':
        return True
    else:
        return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def detect_faces(filename, path , outpath , maskpath):
    """Detects faces in an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    # read the image for the bluring
    img = cv2.imread(path)
    # get width and height of the image
    h, w = img.shape[:2]
    # gaussian blur kernel size depends on width and height of original image
    kernel_width = (w // 55) | 1
    kernel_height = (h // 55) | 1

    # Open an image for the mask and pasted the blure mask and the image
    im = Image.open(path)
    # Create rounded rectangle mask
    mask = Image.new('L', im.size, 0)
    #the Draw allow as to drow on the mask the ellipse of the face
    draw = ImageDraw.Draw(mask)

    for face in faces:
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])
        #print('face bounds: {}'.format(','.join(vertices)))

        start_x = int(vertices[0].split(',')[0].split('(')[1])
        start_y = int(vertices[0].split(',')[1].split(')')[0])
        end_x = int(vertices[2].split(',')[0].split('(')[1])
        end_y = int(vertices[2].split(',')[1].split(')')[0])
        draw.ellipse((start_x, start_y, end_x, end_y), fill=(255))

    mask.save(maskpath+filename)

    blur = cv2.GaussianBlur(img, (kernel_width, kernel_height), 0)
    #convert the cv2 blur to PIL format for pasted them together
    #im_blur = Image.fromarray(blur)
    cv2.imwrite('blure.png', blur, [cv2.IMWRITE_JPEG_QUALITY, 2])
    im_blur = Image.open('blure.png')
    im.paste(im_blur, mask=mask)
    im.save(outpath+filename)
    #img = np.array(im)
    #cv2.imwrite(outpath, img, [cv2.IMWRITE_JPEG_QUALITY, 100])


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def return_json(outPath):
    # creating the json for report
    outJson = []
    # up date the list

    onlyfiles = [f for f in listdir(outPath) if isfile(join(outPath, f))]
    for fileName in onlyfiles:
        im_path = outPath + fileName
        with open(im_path, "rb") as image_file:
            data_base64 = base64.b64encode(image_file.read())
        outJson.append({"fileName": fileName, "base64Format": data_base64.decode("utf-8")})

    # the result is a JSON string:
    outJson = json.dumps(outJson)#,indent=4, sort_keys=False)
    return outJson



@app.route('/blur/', methods=['POST'])
def upload_file_rs():
    if request.method == 'POST':

        files = request.files.getlist("files")

        # create dir for each car session
        now = datetime.now()  # current date and time
        date_time = now.strftime("%d-%m-%Y__%H-%M-%S")
        blurSrcPath = UPLOAD_BASE + date_time
        blurMaskSrcPath = blurSrcPath + '\\Mask_'
        blurOutpath = OUT_BASE + date_time + "\\"
        os.makedirs(blurSrcPath, exist_ok=True)
        os.makedirs(blurOutpath, exist_ok=True)

        
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                file.save(os.path.join(blurSrcPath+'\\',file.filename))

        #choose the script and run the function "go"
        startt0 = time.time()
        for file in files:
            im_path = os.path.join(blurSrcPath+'\\',file.filename)
            print(im_path)
            detect_faces(file.filename,im_path, blurOutpath, blurMaskSrcPath)
        out = return_json(blurOutpath)
        print(len(out))
        #print(out)
        print('Total:', time.time()- startt0)
        return out
    return 'error'






