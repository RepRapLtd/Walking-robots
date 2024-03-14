# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming
#
# $ python3 stream-camera.py
#
# Then navigate a browser to
#
# http://<Robot's_IP_Address>:8000

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import subprocess

def read_file_as_string(filename):
    with open(filename, 'r', encoding='utf-8') as file:  # Open the file
        return file.read()  # Read and return the file's contents as a string
        
def execute_php_file(file_path):
    # Command to execute the PHP file using the PHP CLI
    command = ['php', file_path]
    
    # Execute the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Return the standard output from the PHP script
    return result.stdout


#PAGE=read_file_as_string('index.php')
CSS=read_file_as_string('styles.css')

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = execute_php_file('index.php').encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/styles.css':
            content = CSS.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
        
# Run 2 threads (from GPT4):
'''
import threading
from your_server_module import StreamingServer, StreamingHandler1, StreamingHandler2  # Adjust import as necessary

address1 = ('localhost', 8080)  # Adjust as necessary
address2 = ('localhost', 8081)  # Adjust as necessary

server1 = StreamingServer(address1, StreamingHandler1)
server2 = StreamingServer(address2, StreamingHandler2)

# Define a function to run a server
def run_server(server):
    server.serve_forever()

# Create threads for each server
thread1 = threading.Thread(target=run_server, args=(server1,))
thread2 = threading.Thread(target=run_server, args=(server2,))

# Start the threads
thread1.start()
thread2.start()

# Optionally join the threads to wait for them to finish (they won't, in this case, since they serve forever)
# thread1.join()
# thread2.join()

'''
