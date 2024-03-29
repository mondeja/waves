"""Tests for ``from_datatimes`` generator class method."""

import math
import random

import numpy as np

from waves import Sound


def test_from_datatimes_mono(mono_ttf_gen):
    fps, frequency, volume = (44100, 110, 0.5)

    time_to_frame = mono_ttf_gen(fps=fps, frequency=frequency, volume=volume)
    sound = Sound.from_datatimes(time_to_frame, fps=fps)

    assert sound.n_bytes == 2
    assert sound.n_frames is None
    assert sound.duration == math.inf

    times = [random.uniform(0, 5) for i in range(10)]
    for t in times:
        assert time_to_frame(t) == sound.time_to_frame(t)


def test_from_datatimes_stereo():
    fps, frequencies, volume = (44100, (110, 440), 0.5)
    amplitude = np.iinfo(np.int16).max * volume

    time_to_frame_left = lambda t: (
        np.sin(frequencies[0] * 2 * np.pi * t) * amplitude
    ).astype(np.int16)

    time_to_frame_right = lambda t: (
        np.sin(frequencies[1] * 2 * np.pi * t) * amplitude
    ).astype(np.int16)

    sound = Sound.from_datatimes(
        lambda t: [time_to_frame_left(t), time_to_frame_right(t)], fps=fps
    )

    assert sound.n_bytes == 2
    assert sound.n_frames is None
    assert sound.duration == math.inf

    times = [random.uniform(0, 5) for i in range(10)]
    for t in times:
        frame = sound.time_to_frame(t)
        assert frame[0] == time_to_frame_left(t)
        assert frame[1] == time_to_frame_right(t)
