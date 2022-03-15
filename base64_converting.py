import base64
from PIL import Image
from io import BytesIO

im = 'C:\\Users\\hadas\\Desktop\\spinframe_onWork\\API_function\\blure\\src\\1.jpg'
with open(im, "rb") as image_file:
    data = base64.b64encode(image_file.read())

test_base64_TO_image='C:\\Users\\hadas\\Desktop\\spinframe_onWork\\API_function\\blure\\test_base64_TO_image\\1NEW.png'
im = Image.open(BytesIO(base64.b64decode(data.decode("utf-8"))))
im.save(test_base64_TO_image, 'PNG')

"""
    for fileName in onlyfiles:
        im = cv2.imread(outPath + fileName)
        outJson.append({"fileName": fileName, "base64Format": base64.b64encode(im).decode("utf-8")})

"""