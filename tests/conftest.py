import os

import pytest

from waves import Sound


TESTS_DIR = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def mono_filepath():
    return os.path.join(TESTS_DIR, "files", "mono.wav")


@pytest.fixture
def stereo_filepath():
    return os.path.join(TESTS_DIR, "files", "stereo.wav")


@pytest.fixture
def mono_sound(mono_filepath):
    return Sound.from_file(mono_filepath)


@pytest.fixture
def stereo_sound(stereo_filepath):
    return Sound.from_file(stereo_filepath)
