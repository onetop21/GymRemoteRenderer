import gym, time
import numpy as np
from pystream import RemoteRenderer

env = gym.make('CartPole-v0')
env.reset()
with RemoteRenderer(env, '127.0.0.1', 5555) as renderer:
    env.reset()
    for _ in xrange(100):
        values = env.step(env.action_space.sample())
        renderer.render()
