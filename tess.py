#  from PIL import Image
#  from pytesseract import image_to_string

#  print(image_to_string(Image.open('ots.png')))
#  print(image_to_string(Image.open('ots.png'), lang='eng'))
from PIL import Image
import os
import re
import pytesseract

text = pytesseract.image_to_string(Image.open(os.path.abspath('ots.png')))
# regex extract text before 'trac'
regex = re.compile(r'^([^trac])')
sample = regex.search(text)
print(sample.group(0))
