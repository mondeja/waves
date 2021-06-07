"""Mono sound wave generators tests."""

import numpy as np
import pytest

from waves import Sound


@pytest.mark.parametrize("fps", (44100, 22050), ids=("fps=44100", "22050"))
@pytest.mark.parametrize(
    "frequency",
    (110, 220, 440),
    ids=("frequency=110", "frequency=220", "frequency=440"),
)
@pytest.mark.parametrize(
    "volume",
    (0, 0.5, 1),
    ids=("volume=0", "volume=0.5", "volume=1"),
)
@pytest.mark.parametrize(
    "sample_width", (2, 4), ids=("sample_width=2", "sample_width=4")
)
def test_mono_ttf_gen(mono_ttf_gen, fps, frequency, volume, sample_width):
    time_to_frame = mono_ttf_gen(
        fps=fps,
        frequency=frequency,
        volume=volume,
        sample_width=sample_width,
    )

    sound = Sound.from_datatimes(time_to_frame, fps=fps).with_duration(1)

    assert sound.fps == fps
    assert sound.n_channels == 1
    assert sound.duration == 1
    assert sound.dtype is getattr(np, f"int{sample_width << 3}")
