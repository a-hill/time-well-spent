#!flask/bin/python
from flask import Flask, request, Response
from facemanager import FaceManager
from facerecognitionjob import FaceRecognitionJob
import sys

app = Flask(__name__)

should_load = '--load' in sys.argv
face_manager = FaceManager(should_load)
if should_load:
    print 'Loading from hard copy'


def process_image(request):
    # check that user submitted a file
    if 'upload_file' not in request.files:
        print 'client did not submit a file. ignoring.'
        return None

    # get file
    uploaded_file = request.files['upload_file']

    # read file from stream into array
    image = uploaded_file.stream.read()
    return image


@app.route("/submit_face/entry/", methods=['POST'])
def face_enter():
    print 'Face_Enter'
    image = process_image(request)
    time = int(request.form['time'])
    if image is not None:
        FaceRecognitionJob(image, time, 0, face_manager.entering_faces).run()
        return 'success'
    else:
        return 'fail'


@app.route("/submit_face/exit/", methods=['POST'])
def face_exit():
    print 'Face_Exit'
    img = process_image(request)
    time = int(request.form['time'])
    door = int(request.form['door'])
    if img is not None:
        print'image not none'
        FaceRecognitionJob(img, time, door, face_manager.exiting_faces).run()
        return 'success'
    else:
        print 'image is none : FAIL'
        return 'fail'


@app.route("/cumulative_time/", methods=['GET'])
def get_time():
    f = open('cumulative_time_hard_copy.txt', 'r')
    t = f.read()
    f.close()

    if t == '':
        t = '0'

    resp = Response(t)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/next_exit_time/<int:door>/', methods=['GET'])
def get_exit_time(door):
    queue = face_manager.get_output_queue(door)

    if queue.empty():
        return 'no sound to play'
    else:
        return str(queue.get())


@app.route("/debug/number_faces/", methods=['GET'])
def number_faces():
    text = str(face_manager.get_num_faces())
    resp = Response(text)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# run simply by python server.py
if __name__ == "__main__":
    # Threaded means each request runs in new threads
    # http://bit.ly/2zRX7es
    # Port 5000 is default for flask, if changed need to open port on azure
    app.run(host='0.0.0.0', port=5000, threaded=True)
