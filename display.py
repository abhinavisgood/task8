from flask import Flask, render_template
import cv2
import main
img = input('Enter image loc:   ')
app = Flask(__name__)


@app.route('/')

def home_page():
    global img
    img = cv2.imread(img)
    glow = main.final(img)

    # program code 
    # store final output in opt variable , let say output is "hello world"
    opt =  glow
    return opt
    # y = 4+5                                          
    # return str(y)
if __name__ == "__main__":
    app.run(debug=True, port=1290)