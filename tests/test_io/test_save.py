"""Tests for saving files using ``save`` method."""

import numpy as np

from waves import Sound


def test_save_mono_from_file(mono_sound, tmp_path):
    filename = tmp_path / "save_mono_from_file.wav"

    mono_sound.save(filename)
    assert filename.exists()

    resulting_sound = Sound.from_file(filename.as_posix())
    assert np.array_equal(resulting_sound.data, mono_sound.data)


def test_save_stereo_from_file(stereo_sound, tmp_path):
    filename = tmp_path / "save_stereo_from_file.wav"

    stereo_sound.save(filename)
    assert filename.exists()

    resulting_sound = Sound.from_file(filename.as_posix())
    assert np.array_equal(resulting_sound.data, stereo_sound.data)


def test_save_mono_from_function(tmp_path):
    fps, frequency, volume = (44100, 110, 0.5)
    amplitude = np.iinfo(np.int16).max * volume

    def time_to_frame(t):
        return (np.sin(frequency * 2 * np.pi * t) * amplitude).astype(np.int16)

    mono_sound = Sound.from_datatimes(time_to_frame, fps=fps).with_duration(0.5)

    filename = tmp_path / "save_mono_from_function.wav"
    mono_sound.save(filename)
    assert filename.exists()

    resulting_sound = Sound.from_file(filename)
    assert np.array_equal(resulting_sound.data, mono_sound.data)


def test_save_stereo_from_function(tmp_path):
    fps, frequencies, volume = (44100, (110, 440), 0.5)
    amplitude = np.iinfo(np.int16).max * volume

    time_to_frame_left = lambda t: (
        np.sin(frequencies[0] * 2 * np.pi * t) * amplitude
    ).astype(np.int16)

    time_to_frame_right = lambda t: (
        np.sin(frequencies[1] * 2 * np.pi * t) * amplitude
    ).astype(np.int16)

    stereo_sound = Sound.from_datatimes(
        lambda t: [time_to_frame_left(t), time_to_frame_right(t)], fps=fps
    ).with_duration(0.5)

    filename = tmp_path / "save_stereo_from_function.wav"
    stereo_sound.save(filename)
    assert filename.exists()

    resulting_sound = Sound.from_file(filename)
    assert np.array_equal(resulting_sound.data, stereo_sound.data)
