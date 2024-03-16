# 
# Raspberry Pi Camera server
#
# Written by GPT4
# Licence: GPL
#
# Adrian Bowyer
# RepRap Lyd
# https://reprapltd.com
#
# Run this with
# 
# $ python3 camera-server.py &
#
# The camera stream can then be embedded in a web page with
#
# <?php include 'camera_ip.php'; ?>
# <img src="http://<?= $camera_ip; ?>:8000/stream.mjpg" width="640" height="480">
#

from flask import Flask, Response
import picamera
import io
from time import sleep
import socket

app = Flask(__name__)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_php_script(ip_address):
    php_content = f"""<?php
// Auto-generated IP address for camera stream
$camera_ip = "{ip_address}";
?>
"""
    with open("camera_ip.php", "w") as php_file:
        php_file.write(php_content)

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
    ip_address = get_ip_address()
    generate_php_script(ip_address)
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
    
