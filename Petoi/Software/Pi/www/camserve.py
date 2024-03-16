from flask import Flask, Response
import picamera
import io
from time import sleep

app = Flask(__name__)

def generate_camera_stream():
    with picamera.PiCamera() as camera:
        # Camera warm-up time
        sleep(2)
        
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            frame = stream.read()
            
            # Use a multipart response format (MJPEG)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            stream.seek(0)
            stream.truncate()

@app.route('/stream.mjpg')
def stream_mjpg():
    return Response(generate_camera_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
