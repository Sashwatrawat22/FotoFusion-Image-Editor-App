from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os
from main2 import second
from main3 import third
from main4 import fourth

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'pdf', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'

app.register_blueprint(second,url_prefix="/Stylize")
app.register_blueprint(third,url_prefix="/FaceSwap")
app.register_blueprint(fourth, url_prefix="/TakePicture")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f'The operation is {operation} and filename is {filename}')
    img=cv2.imread(f"uploads/{filename}")

    if operation == "cgray":
        imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newFilename = f"static/converted/{filename}"
    else:
        new_extension = {
            "cwebp": "webp",
            "cjpg": "jpg",
            "cpng": "png"
        }[operation]
        newFilename = f"static/converted/{filename.rsplit('.', 1)[0]}.{new_extension}"

    cv2.imwrite(newFilename, imgProcessed if operation == "cgray" else img)
    return newFilename
    pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Stylize")
def style():
    return render_template("index2.html")

@app.route("/FaceSwap")
def face_swap():
    return render_template("index3.html")

@app.route("/TakePicture")
def take_picture():
    return render_template("index4.html")

@app.route("/edit", methods=['GET','POST'])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation)
            flash(f"Your image has been processed and is available here <a href='/{new}' target='_blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")


app.run(debug=True)