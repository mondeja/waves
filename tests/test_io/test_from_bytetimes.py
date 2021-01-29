"""Tests for opening sounds using ``from_bytetimes`` class method."""

import struct
import wave

import numpy as np

from waves import Sound


def test_from_bytetimes_mono(mono_filepath):
    with wave.open(mono_filepath, "rb") as f:
        hexdata, fps, n_frames = (f.readframes(-1), f.getframerate(), f.getnframes())

    hexframes = []
    for bytes_frame in struct.iter_unpack(f"{f.getsampwidth()}c", hexdata):
        hexframes.append(b"".join(bytes_frame))
        
    time_to_hexframe = lambda t: hexframes[int(round(t * fps))]
    sound = Sound.from_bytetimes(time_to_hexframe, fps=fps)
    
    for i, t in enumerate(sound.time_sequence):
        try:
            frame = sound.time_to_frame(t)
        except IndexError:
            assert i == n_frames
            break
    
        hexframe = time_to_hexframe(t)
        assert frame == np.frombuffer(hexframe, dtype=np.int16)[0]


def test_from_bytetimes_stereo(stereo_filepath):
    with wave.open(stereo_filepath, "rb") as f:
        hexdata, fps, n_frames = (f.readframes(-1), f.getframerate(), f.getnframes())
        n_channels, n_bytes = (f.getnchannels(), f.getsampwidth())

    hexframes = []
    for bytes_frame in struct.iter_unpack(f"{n_bytes * n_channels}c", hexdata):
        hexframe = []
        for channel_index in range(n_channels):
            start = channel_index * n_bytes
            end = start + n_bytes
            hexframe.append(b"".join(bytes_frame[start: end]))
        hexframes.append(hexframe)

    time_to_hexframe = lambda t: hexframes[int(round(t * fps))]
    sound = Sound.from_bytetimes(time_to_hexframe, fps=fps)
    
    for i, t in enumerate(sound.time_sequence):
        try:
            frame = sound.time_to_frame(t)
        except IndexError:
            assert i == n_frames
            break

        hexframe = time_to_hexframe(t)
        assert frame[0] == np.frombuffer(hexframe[0], dtype=np.int16)[0]
        assert frame[1] == np.frombuffer(hexframe[1], dtype=np.int16)[0]   