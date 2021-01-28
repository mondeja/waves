"""Tests for ``from_dataframes`` generator class method."""

import numpy as np

import pytest

from waves import Sound

@pytest.mark.parametrize(
    "explicit_n_frames",
    (True, False),
    ids=("explicit `n_frames` kwarg", "implicit `n_frames` kwarg")
)
def test_from_dataframes_mono(mono_sound, explicit_n_frames):
    frames = mono_sound.data
    
    sound = Sound.from_dataframes(
        lambda i: frames[i], fps=mono_sound.fps,
        n_frames=mono_sound.n_frames if explicit_n_frames else None,
    )

    assert np.array_equal(frames, sound.data)
    assert mono_sound.n_frames == sound.n_frames


@pytest.mark.parametrize(
    "explicit_n_frames",
    (True, False),
    ids=("explicit `n_frames` kwarg", "implicit `n_frames` kwarg")
)
def test_from_dataframes_stereo(stereo_sound, explicit_n_frames):
    frames = stereo_sound.data
    frames_T = frames.T
    
    sound = Sound.from_dataframes(
        lambda i: frames_T[i],
        fps=stereo_sound.fps,
        n_frames=stereo_sound.n_frames if explicit_n_frames else None,
    )
    
    assert np.array_equal(frames, sound.data)
    assert stereo_sound.n_frames == sound.n_frames
    