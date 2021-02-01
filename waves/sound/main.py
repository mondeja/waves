"""Mono sound."""
import math
from functools import partial

import numpy as np

from waves.sound.io import SoundIO


class Sound(SoundIO):
    """Base class for a sound.

    It's not intended to be instanciated directly. Instead, use the class methods
    :py:meth:`waves.Sound.from_file`, :py:meth:`waves.Sound.from_sndbuffer`.

    Parameters
    ----------

    n_frames : int, optional
      Number of frames of the audio data.

    n_bytes : int, optional
      Sample width of the sound.

    n_channels : int, optional
      Number of channels of the sound.

    fps : int, optional
      Number of frames per second, also known as *framerate* or *sampling rate*.

    dtype : type, optional
      Type of the data used to decode the sound as a Numpy array. This should match
      with the number of bits of sample width for optimal performance and memory
      management.

    filename : str, optional
      Path to the file located in disk which stores the raw sound data.

    f : pysndfile.PySndfile, optional
      Opened file descriptor of the file located in disk which stores the raw sound
      data.

    time_to_frame : function, optional
      Function which takes a time ``t`` for each frame of the sound and renders the
      Numpy array data of the sound for each frame. Only defined if the sound has been
      created an interpolator function.

    metadata : dict, optional
      Dictionary with metadata about the sound.
    """

    def __init__(
        self,
        n_frames=None,
        n_bytes=2,
        n_channels=None,
        fps=44100,
        dtype=np.int16,
        filename=None,
        f=None,
        time_to_frame=None,
        metadata={},
    ):
        #: Number of frames of the audio data.
        self.n_frames = n_frames

        #: Sample width of the sound.
        self.n_bytes = n_bytes

        #: Number of channels of the sound.
        self.n_channels = n_channels

        #: Number of frames per second, also known as *framerate* or *sampling rate*.
        self.fps = fps

        #: Type of the data used to decode the sound as a Numpy array.
        self.dtype = dtype

        #: Path to the file located in disk which stores the raw sound data.
        self.filename = filename
        self.f = f

        #: Function which takes a time ``t`` for each frame of the sound and renders the
        #: Numpy array data of the sound for each frame. Only defined if the sound has
        #: been created an interpolator function.
        self.time_to_frame = time_to_frame

        #: Dictionary with metadata about the sound.
        self.metadata = metadata

    @property
    def n_bits(self):
        """Returns the number of bits for the width of the sound."""
        return self.n_bytes << 3

    @property
    def duration(self):
        """Returns the duration of the sound, in seconds.

        If the sound has been created using functions and you don't have extracted
        the data before by calling :py:property:`Sound.data`, the returned duration
        will be infinite.
        """
        return (self.n_frames / self.fps) if self.n_frames else math.inf

    @duration.setter
    def duration(self, duration):
        self.n_frames = int(duration * self.fps)

    def with_duration(self, duration):
        self.n_frames = int(duration * self.fps)
        return self

    @property
    def time_sequence(self):
        """Generates a linear range which represents the sequence for the time of
        the sound.

        The range will be infinite for sounds created using functions (only if you
        haven't extracted the data before by calling :py:property:`Sound.data`),
        so you must break the generation at some point or this will result in a
        infinite loop.
        """
        duration, n, step = (self.duration, 0, 1 / self.fps)
        while n < duration:
            yield n
            n += step

    def __getattr__(self, name):
        if name == "plot":
            from waves.sound.plot import plot

            return partial(plot, self)
        elif name == "play":
            from waves.sound.play import play

            return partial(play, self)
        elif name == "figure":
            from waves.sound.figure import figure

            return partial(figure, self)
        return super().__getattr__(name)
