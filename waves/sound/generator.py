import functools

import numpy as np


@functools.lru_cache(maxsize=None)
def mono_ttf_gen(fps=44100, frequency=110, volume=0.5):
    """Generates a ``time_to_frame`` function for a mono sine wave which can be
    passed to ``Sound.from_datatimes``.


    Parameters
    ----------

    fps : int, optional
      Frames per second of the sound to generate.

    frequency : int, optional
      Frequency of the sine wave.

    volume : float, optional
      Value between 0 and 1 that will define the volume of the wave.


    Returns
    -------

    function: Takes a parameter time ``t`` and returns the sound data for that
        time.


    Examples
    --------
    >>> from waves import Sound, mono_ttf_gen
    >>>
    >>> time_to_frame = mono_ttf_gen(frequency=660, volume=0.2)
    >>> sound = Sound.from_datatimes(time_to_frame).with_duration(2)
    """
    amplitude = np.iinfo(np.int16).max * volume

    def time_to_frame(t):
        return (np.sin(frequency * 2 * np.pi * t) * amplitude).astype(np.int16)

    return time_to_frame


@functools.lru_cache(maxsize=None)
def stereo_ttf_gen(fps=44100, frequencies=(440, 110), volume=0.5):
    """Generates a ``time_to_frame`` function for a stereo sine wave which can be
    passed to ``Sound.from_datatimes``.


    Parameters
    ----------

    fps : int, optional
      Frames per second of the sound to generate.

    frequencies : tuple or list, optional
      Frequencies of each channel for the sine wave. The number of channels
      will be determined by the number of values introduced in this parameter.

    volume : float, optional
      Value between 0 and 1 that will define the volume of the wave.


    Returns
    -------

    function: Takes a parameter time ``t`` and returns the sound data for that
        time for each channel of the sound.


    Examples
    --------
    >>> from waves import Sound, stereo_ttf_gen
    >>>
    >>> time_to_frame = stereo_ttf_gen(frequencies=(660, 290), volume=0.2)
    >>> sound = Sound.from_datatimes(time_to_frame).with_duration(2)
    """
    amplitude = np.iinfo(np.int16).max * volume

    def time_to_frame(t):
        return [np.sin(freq * 2 * np.pi * t) * amplitude for freq in frequencies]

    return time_to_frame
