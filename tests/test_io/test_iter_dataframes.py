"""Tests for ``iter_dataframes`` generator property."""

import numpy as np

from waves import Sound


def test_iter_dataframes_mono_from_file(mono_sound):
    data = mono_sound.dataframes
    
    for i, frame in enumerate(mono_sound.iter_dataframes):
        assert frame == data[i]


def test_iter_dataframes_stereo_from_file(stereo_sound):
    data = stereo_sound.dataframes
    
    for i, frame in enumerate(stereo_sound.iter_dataframes):
        assert frame[0] == data[i][0]
        assert frame[1] == data[i][1]


def test_iter_dataframes_mono_from_function():
    fps, frequency, volume = (44100, 110, .5)
    amplitude, t_fps = (np.iinfo(np.int16).max * volume, 1 / fps)

    def time_to_frame(t):
        return (np.sin(frequency * 2 * np.pi * t) * amplitude).astype(
            np.int16
        )

    sound = Sound.from_datatimes(time_to_frame, fps=fps).with_duration(.5)
    for i, frame in enumerate(sound.iter_dataframes):
        assert frame == time_to_frame(i * t_fps)
    

def test_iter_dataframes_stereo_from_function():
    fps, frequencies, volume  = (44100, (110, 440), .5)
    amplitude, t_fps = (np.iinfo(np.int16).max * volume, 1 / fps)
    
    time_to_frame_left = lambda t: (np.sin(
        frequencies[0] * 2 * np.pi * t
    ) * amplitude).astype(np.int16)
    
    time_to_frame_right = lambda t: (np.sin(
        frequencies[1] * 2 * np.pi * t
    ) * amplitude).astype(np.int16)

    sound = Sound.from_datatimes(
        lambda t: [time_to_frame_left(t), time_to_frame_right(t)], fps=fps
    ).with_duration(.5)
    
    for i, frame in enumerate(sound.iter_dataframes):
        assert frame[0] == time_to_frame_left(i * t_fps)
        assert frame[1] == time_to_frame_right(i * t_fps)
