import wave
import random
import struct
import sys

import numpy as np
import matplotlib.pyplot as plt

from waves import Sound

"""
import pygame
pygame.mixer.quit()
pygame.mixer.init()

pygame.mixer.music.load("kick1.wav")
pygame.mixer.music.play()


with wave.open("kick1.wav", "r") as f:
    nchannels, sampwidth, framerate, nframes, comptype, compname = f.getparams()
    print(nchannels, sampwidth, framerate, nframes)
    
    hexdata = f.readframes(nframes)
    data = np.frombuffer(hexdata, np.int16)
    data.shape = (-1, 2)
    data = data.T
    
    duration = 1 / framerate
    t_seq = np.arange(0, nframes / framerate, duration)
    
    fig, axs = plt.subplots(2)
    fig.suptitle('Vertically stacked subplots')
    axs[0].plot(t_seq, data[0])
    axs[1].plot(t_seq, data[1])
    plt.show()
"""


import sys
from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType


def getsize(obj):
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size

"""
from waves import Sound

with wave.open("stereo.wav") as f:
    print(f.readframes(2))
    f.setpos(0)
sound = Sound.from_file("mono.wav")
sound.play()

for bytes in sound.iter_dataframes(int(44100 / 4)):
    print(bytes)

#sound = Sound.from_file("mono.wav")
SAMPLE_LEN = 3
"""
"""
values = []

for i in range(0, SAMPLE_LEN):
    value = random.randint(-32767, 32767)
    print(value)
    packed_value = struct.pack('h', value)
    values.append(packed_value)
    values.append(packed_value)
print(values)
"""

"""
import pysndfile as snd

sound = Sound.from_file("tests/files/stereo.wav")
sound.play(wait=False)
sound.plot()
"""
"""
make_frame = lambda t: np.array([
    np.sin(440 * 2 * np.pi * t),
    np.sin(880 * 2 * np.pi * t),
]).T.copy(order="C"),
"""

# mono
"""
duration, fps, frequency, volume = (3, 44100, 110, 0.5)
t = np.linspace(0., duration, duration * fps)
amplitude = np.iinfo(np.int16).max * volume
data = (amplitude * np.sin(frequency * 2. * np.pi * t)).astype(np.int16)
sound = Sound.from_dataframes(lambda i: data[i], fps=fps)

# stereo
duration, fps, frequencies, volume = (3, 44100, (110, 440), 0.5)
t = np.linspace(0., duration, duration * fps)
amplitude = np.iinfo(np.int16).max * volume
data_left = (amplitude * np.sin(frequencies[0] * 2. * np.pi * t)).astype(np.int16)
data_right = (amplitude * np.sin(frequencies[1] * 2. * np.pi * t)).astype(np.int16)
sound = Sound.from_dataframes(lambda i: np.array([data_left[i], data_right[i]]), fps=fps)
"""

# stereo
# mono generating sine wave
import numpy as np
from waves import Sound

duration, fps, frequency, volume = (3, 44100, 110, 0.5)
amplitude = np.iinfo(np.int16).max * volume

def time_to_frame(t):
    return (np.sin(frequency * 2 * np.pi * t) * amplitude).astype(
        np.int16
    )

sound = Sound.from_datatimes(time_to_frame, fps=fps).with_duration(duration)
sound.play()

