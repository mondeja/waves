"""Tests for reading WAV files as Numpy arrays using ``data`` property."""


def test_data_mono(mono_sound):
    data = mono_sound.data
    
    assert data.shape[0] == 106022
    assert data[0].nbytes == 2


def test_data_stereo(stereo_sound):
    data = stereo_sound.data
    
    assert data.shape[0] == 2
    assert data.shape[1] == 55216
    assert data[0][0].nbytes == 2
