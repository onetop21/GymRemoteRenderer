import sys, os, argparse, zmq, time, threading, socket, numpy as np, Tkinter as tk
from PIL import Image, ImageTk

class RemoteRenderer:
    def __init__(self, env, address='localhost', port=5555):
        self.env = env
        self.address = address
        self.port = port
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.DEALER)

    def __enter__(self):
        self.sock.setsockopt(zmq.LINGER, 1000)
        self.sock.connect('tcp://{}:{}'.format(self.address, self.port))
        return self

    def __exit__(self, ty, va, tb):
        self.sock.disconnect('tcp://{}:{}'.format(self.address, self.port))
        self.sock.close()
        
    def render(self):
        framebuffer = self.env.render(mode='rgb_array')
        self.sock.send(np.array(framebuffer.shape), flags=zmq.SNDMORE)
        self.sock.send(framebuffer.copy(order='C'))

class StreamVideo(threading.Thread):
    def __init__(self, callback, title='StreamVideo', width=600, height=400):
        threading.Thread.__init__(self)
        self.daemon=True
        
        self.title = title 
        self.handle = tk.Tk()
        self.handle.title(self.title)
        self.handle.resizable(width=False, height=False)
        self.geometry(width, height)
        #self.handle.attributes('-toolwindow', 1)

        self.frame = tk.Label(self.handle)
        self.frame.pack()

        self.callback = callback

    def geometry(self, width, height):
        self.handle.geometry('{}x{}'.format(width, height))

    def render(self, framebuffer):
        image = Image.fromarray(framebuffer)
        framebuffer = ImageTk.PhotoImage(image)
        self.frame.config(image=framebuffer)
        self.frame.image=framebuffer

        self.handle.title(self.title + ' [{}fps]'.format(1/(time.time() - self.tick)))
        self.tick = time.time()

    def run(self):
        self.tick = time.time()
        while True:
            framebuffer = self.callback()
            if isinstance(framebuffer, np.ndarray): 
                self.geometry(len(framebuffer[0]), len(framebuffer))
                self.render(framebuffer)

    def show(self):
        self.start()
        self.handle.mainloop()

def _get_ip_addr():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    return sock.getsockname()[0]


# Main
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=5555, help='Port number to open stream server. Default is 5555')
args = parser.parse_args()

if __name__ == '__main__':
    ip_addr = _get_ip_addr()
    port = args.port 

    context = zmq.Context()
    sock = context.socket(zmq.DEALER)
    sock.setsockopt(zmq.RCVTIMEO, 1000)
    sock.bind('tcp://*:%d'%port)

    print 'OpenAI gym Streamer by onetop21'
    print 'Address: {}:{}'.format(ip_addr, port)

    def receivePacket():
        try:
            framesize = np.frombuffer(sock.recv(), dtype='int64')
            return np.frombuffer(sock.recv(), dtype='uint8').reshape(framesize[0], framesize[1], framesize[2])
        except Exception:
            return None

    test = StreamVideo(receivePacket, 'OpenAI Streamer')
    test.show()


