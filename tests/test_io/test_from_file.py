"""Tests for opening a wav file from file path."""

import numpy as np

from waves import Sound

import pysndfile as snd


def test_from_file_mono(mono_filepath):
    sound = Sound.from_file(mono_filepath)
    
    assert sound.n_frames == 106022
    assert sound.n_bytes == 2
    assert sound.n_bits == 16
    assert sound.fps == 44100
    assert sound.n_channels == 1
    assert sound.dtype is np.int16
    
    assert sound.time_to_frame is None
    assert sound.filename == mono_filepath.encode("utf-8")
    assert isinstance(sound.f, snd.PySndfile)
    
    assert isinstance(sound.metadata, dict)
    assert sound.metadata["SF_STR_SOFTWARE"] == (
        b"Adobe Soundbooth CS5 (XMPDocOpsTemporal:2008.08.26)"
    )
    assert sound.metadata["SF_STR_ARTIST"] == b"freewavesamples.com"
    assert sound.metadata["SF_STR_DATE"] == b"2015-05-06T19:28:12-07:00"


def test_from_file_stereo(stereo_filepath):
    sound = Sound.from_file(stereo_filepath)
    
    assert sound.n_frames == 55216
    assert sound.n_bytes == 2
    assert sound.n_bits == 16
    assert sound.fps == 44100
    assert sound.n_channels == 2
    assert sound.dtype is np.int16
    
    assert sound.time_to_frame is None
    assert sound.filename == stereo_filepath.encode("utf-8")
    assert isinstance(sound.f, snd.PySndfile)
    
    assert isinstance(sound.metadata, dict)
    assert sound.metadata["SF_STR_TITLE"] == b"Bass Drum 1"
    assert sound.metadata["SF_STR_ARTIST"] == b"freewavesamples.com"
    assert sound.metadata["SF_STR_DATE"] == b"2015"
