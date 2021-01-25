"""Stereo sound."""
import wave

import numpy as np

from waves.sound.mono import MonoSound
from waves.sound.playable import PlayableSound
from waves.sound.plottable import PlottableSound
from waves.sound.io import SoundIO



class StereoSound(SoundIO, PlayableSound, PlottableSound):
    """Represents a sound, in one or multiple channels.
    
    Instanciate this class directly of call one of their class methods.
    
    Parameters
    ----------
    
    channels : array[np.ndarray]
      Arrays of sound data, one for each channel.
    """

    def __init__(self, channels=None, f=None, filename=None):
        self.channels = channels

        self.f = f
        self.filename = filename
    
    @property
    def fps(self):
        """Returns the maximum number of frames per second, also known as "framerate"
        or "sampling rate", of the channels which composes the sound.
        """
        return max(channel.fps for channel in self.channels)
    
    @property
    def n_bytes(self):
        """Returns the number of bytes used by the data of the sound."""
        return self.channels[0].n_bytes
    
    @property
    def n_bits(self):
        """Returns the number of bits used by the data of the sound."""
        return self.channels[0].n_bits
    
    @property
    def n_frames(self):
        """Returns the total number of frames of which the sound is composed."""
        return max(channel.n_frames for channel in self.channels)

    @property
    def n_channels(self):
        """Returns the number of mono channels of which the sound is composed."""
        return len(self.channels)

    @property
    def duration(self):
        """Returns the duration of the sound, in seconds."""
        return max(channel.duration for channel in self.channels)
    
    @property
    def time_sequence(self):
        return self.channels[0].time_sequence
    
    def time_to_frame(self, t):
        return [
            channel.time_to_frame(t) for channel in self.channels
        ]


Sound = StereoSound
