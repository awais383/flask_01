from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# Load the pre-trained Haar Cascade face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Create a recognizer using LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

known_face_ids = {
    1: "Awais",
    2: "Shehzad"
}

def train_recognizer():
    image_paths = ['awais/awais.jpeg', 'shehzad/shehzad.jpeg']
    face_samples = []
    ids = []

    for image_path in image_paths:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            face_samples.append(gray[y:y+h, x:x+w])
            ids.append(len(face_samples)) 

    recognizer.train(face_samples, np.array(ids))
    recognizer.save('trainer.yml') 

train_recognizer()

recognizer.read('trainer.yml')

face_locations = []
face_names = []
process_this_frame = True

def gen_frames():
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            face_names = []
            for (x, y, w, h) in faces:
                id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

                if confidence < 100:
                    name = known_face_ids.get(id_, "Awais")
                else:
                    name = "Shehzad"
                
                face_names.append(name)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, name, (x + 6, y - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('live_stream.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
