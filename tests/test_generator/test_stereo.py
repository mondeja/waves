"""Stereo sound wave generators tests."""

import pytest

from waves import Sound


@pytest.mark.parametrize("fps", (44100, 22050), ids=("fps=44100", "22050"))
@pytest.mark.parametrize(
    "frequencies",
    ((110, 220), (440, 880), (120, 360, 720)),
    ids=("frequency=110", "frequency=220", "frequency=440"),
)
@pytest.mark.parametrize(
    "volume",
    (0, 0.5, 1),
    ids=("volume=0", "volume=0.5", "volume=1"),
)
def test_stereo_ttf_gen(stereo_ttf_gen, fps, frequencies, volume):
    time_to_frame = stereo_ttf_gen(fps=fps, frequencies=frequencies, volume=volume)

    sound = Sound.from_datatimes(time_to_frame, fps=fps).with_duration(1)

    assert sound.fps == fps
    assert sound.n_channels == len(frequencies)
    assert sound.duration == 1
