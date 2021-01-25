"""Mono sound."""
import numbers
import time

import matplotlib.pyplot as plt
import numpy as np

from waves.sound.playable import PlayableSound
from waves.sound.plottable import PlottableSound
from waves.sound.io import SoundIO


class MonoSound(SoundIO, PlayableSound, PlottableSound):
    """Base class for a channel of sound.
    
    Parameters
    ----------
    
    n_frames : int
      Number of frames of the audio data.
    
    n_bytes : int, optional
      Sample width of the sound. Should be one of: ``1``, ``2``, ``4``, ``8``.
    
    fps : int, optional
      Number of frames per second, also known as "framerate" or "sampling rate".
    """
    def __init__(
        self,
        n_frames=None,
        n_bytes=2,
        fps=44100,
        filename=None,
        f=None,
        time_to_frame=None
    ):
        self.n_frames = n_frames
        self.n_bytes = n_bytes
        self.fps = fps

        self.filename = filename
        self.f = f
        self.time_to_frame = time_to_frame
        
        self.n_channels = 1

    @property
    def n_bits(self):
        """Returns the number of bits for the width of the sound."""
        return self.n_bytes ** 4
        
    @property
    def duration(self):
        """Returns the duration of the sound, in seconds."""
        return self.n_frames / self.fps
    
    @property
    def time_sequence(self):
        """Returns a linear range which represents the sequence for the time
        of the sound.
        """
        for frame in np.arange(0, self.duration, 1 / self.fps):
            yield frame
