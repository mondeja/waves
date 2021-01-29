"""Tests for reading WAV files as Numpy arrays using ``dataframes`` property."""


def test_dataframes_mono(mono_sound):
    dataframes = mono_sound.dataframes
    
    assert dataframes.shape[0] == 106022
    assert dataframes[0].nbytes == 2


def test_dataframes_stereo(stereo_sound):
    dataframes = stereo_sound.dataframes
    
    assert dataframes.shape[0] == 55216
    assert dataframes.shape[1] == 2
    assert dataframes[0][0].nbytes == 2
