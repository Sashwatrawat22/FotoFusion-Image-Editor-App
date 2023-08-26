from flask import Blueprint, Flask, render_template, Response, url_for, redirect, flash
import cv2
import base64, os

app = Flask(__name__)
app.secret_key = 'super secret key'

# Create a Blueprint instance
fourth = Blueprint("fourth", __name__)

cap = cv2.VideoCapture(0)
captured_frame = None

def generate_frames():
    global captured_frame
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@fourth.route('/')
def index():
    return render_template("index4.html")

@fourth.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@fourth.route('/capture', methods=['POST'])
def capture():
    global captured_frame
    _, captured_frame = cap.read()  # Capture a frame
    
    # Save the captured image
    image_filename = os.path.join(app.root_path, "static", "captured_images", "captured.jpg")
    cv2.imwrite(image_filename, captured_frame)
    
    flash("Your image has been captured. You can view it <a href='/fourth/view_picture' target='_blank'>here</a>.")
    return redirect(url_for('fourth.index'))

@fourth.route('/view_picture')
def view_picture():
    image_filename = "captured.jpg"  # No need for the full path
    return render_template("picture.html", image_filename=image_filename)