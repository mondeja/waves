"""Tests for ``iter_datatimes`` generator property."""

import numpy as np

from waves import Sound


def test_iter_datatimes_mono_from_file(mono_sound):
    data = mono_sound.dataframes

    zipped = zip(mono_sound.iter_datatimes, mono_sound.time_sequence)
    for i, ((id_t, frame), ts_t) in enumerate(zipped):
        assert id_t == ts_t
        assert data[i] == frame


def test_iter_datatimes_stereo_from_file(stereo_sound):
    data = stereo_sound.dataframes

    zipped = zip(stereo_sound.iter_datatimes, stereo_sound.time_sequence)
    for i, ((id_t, frame), ts_t) in enumerate(zipped):
        assert id_t == ts_t
        assert data[i][0] == frame[0]
        assert data[i][1] == frame[1]


def test_iter_datatimes_mono_from_function(mono_ttf_gen):
    fps, frequency, volume = (44100, 110, 0.5)

    time_to_frame = mono_ttf_gen(fps=fps, frequency=frequency, volume=volume)
    sound = Sound.from_datatimes(time_to_frame, fps=fps).with_duration(0.5)

    zipped = zip(sound.iter_datatimes, sound.time_sequence)
    for (id_t, frame), ts_t in zipped:
        assert id_t == ts_t
        assert time_to_frame(ts_t) == frame


def test_iter_datatimes_stereo_from_function():
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
    ).with_duration(0.5)

    zipped = zip(sound.iter_datatimes, sound.time_sequence)
    for (id_t, frame), ts_t in zipped:
        assert id_t == ts_t
        assert time_to_frame_left(ts_t) == frame[0]
        assert time_to_frame_right(ts_t) == frame[1]
