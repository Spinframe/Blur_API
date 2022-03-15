# importing the requests library
import requests
import base64
from PIL import Image
from io import BytesIO

src = 'C:\\Users\\hadas\\Desktop\\spinframe_onWork\\API_function\\blure\\src\\'
url = 'http://10.0.0.3:5000/blur/'
multiple_files = [('files', ('1.jpg', open(src+'1.jpg', 'rb'), 'image/png')),
                      ('files', ('2.jpg', open(src+'2.jpg', 'rb'), 'image/png')),
                      ('files', ('3.jpg', open(src+'3.jpg', 'rb'), 'image/png')),
                      ('files', ('4.jpg', open(src+'4.jpg', 'rb'), 'image/png')),
                      ('files', ('5.jpg', open(src+'5.jpg', 'rb'), 'image/png')),
                      ('files', ('6.jpg', open(src+'6.jpg', 'rb'), 'image/png')),
                      ('files', ('7.jpg', open(src+'7.jpg', 'rb'), 'image/png')),
                      ('files', ('8.jpg', open(src+'8.jpg', 'rb'), 'image/png'))
                      ]

r = requests.post(url, files=multiple_files)

j = r.json()
print(j[0]['fileName'])
test_base64_TO_image='C:\\Users\\hadas\\Desktop\\spinframe_onWork\\API_function\\blure\\test_base64_TO_image\\'

for i in range(len(j)):
    data = j[0]['base64Format']
    im = Image.open(BytesIO(base64.b64decode(data)))
    filename = test_base64_TO_image + j[i]['fileName'].split('.')[0] + '.png'
    im.save(filename, 'PNG')


