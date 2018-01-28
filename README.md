# GymRemoteRenderer
Remote Renderer for OpenAI Gym.
This code for solving a problem as below line to run open ai gym application on remote system like AWS.
<pre>pyglet.canvas.xlib.NoSuchDisplayException: Cannot connect to "None"</pre>

# Preparation
Need to install packages.
<pre>
pip install numpy zmq pillow
</pre>
Need to install xvfb-run application.
<pre>
sudo apt-get install xvfb
</pre>
# How to use
## Server
  Run pystream.py on local system.
  If you want to change port, run with argument -p <port number>.
  <pre><code>python ./pystream.py -p 5555</code></pre>
## Client
  Import RemoteRenderer from pystream to your code.
  <pre><code>from pystream import RemoteRenderer</code></pre>
  And create instance by with syntax.
  If you want to changel IP address and port of server, 
  create instance with address and port parameters.
  <pre>with RemoteRenderer(env, address='192.168.0.101', port=5555) as renderer:</pre>
### Example
<pre>import gym 
import numpy as np
from pystream import RemoteRenderer

env = gym.make('CartPole-v0')
with RemoteRenderer(env) as renderer:
    env.reset()
    for _ in xrange(100):
        values = env.step(env.action_space.sample())
        renderer.render()
</pre>
### Run script
To avoid pyglet.canvas.xlib.NoSuchDisplayException, run on virtual frame buffer by xvfb.
You can run script using xvfb.sh easily.
<pre>./xvfb.sh [script file]</pre>
