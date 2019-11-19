from PIL import Image
import pytesseract
import cv2
from dateutil.parser import parse
import re
from flask import Flask, request, jsonify, render_template

import base64
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process',methods=['POST'])

def process():
    #print('started')
    #imgdata = base64.b64decode(path)
    #filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    #with open(filename, 'wb') as f:
        #f.write(imgdata)
    if request.method == 'POST':
        message = request.form['experience']
        imgdata = message
    #imgdata=request.form.value()
        imgdata = base64.b64decode(imgdata)
        filename = 'some_image.png'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(imgdata)

            im = cv2.imread(filename)
    # im = Image.open(f1)

            text = pytesseract.image_to_string(im, lang=None)
            text = " ".join(text.split())
            for wor in text.split("\n"):
                text = re.sub(r"[{ )}> @ ? !+ _:= # )(]", ' ', text)
                text = re.sub(r"d{5,}", "", text)
                text = re.sub(r" {2,}", "", text)
        # text = re.sub("\\b\s\w{2,}\d{1,}\\b", "", text).strip()


        # regEx = r'(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?(?:(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|MAY|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:(?:-|/)|(?:,|\.)?\s)?)?(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?)(?:\d{2,4})'
                regEx = r'(?:\d{1,2}(?:(?:-|/)|(?:th|st|nd|rd)?\s))?(?:(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|MAY |Jun(?:e)?|Jul(?:y)?|ju1|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(?:(?:- |-| |/)|(?:,|\.)?\s)?)?(?:\d{1,2}(?:(?:-|, |,| |/)|(?:th|st|nd|rd)?\s))?)(?:\d{2,4})'
                result = re.findall(regEx, text)

            for i in result:

                if (len(i) >= 8):
                    try:
                        date = parse(i)
                        date=date.strftime("%Y-%m-%d")
                        return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(date))
                    except:
                        pass
        return 'null'


if __name__ == '__main__':
    app.run(debug=True)

   # path_ = input("enter image path")
    #process(path_)
