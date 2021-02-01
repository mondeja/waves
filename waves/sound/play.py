"""Playable sounds interface."""
import numpy as np

from waves.players.pygame import play_sound


def play(sound, wait=True, **kwargs):
    return play_sound(
        sound.dataframes,
        frequency=sound.fps,
        size=(sound.n_bytes << 3)
        * (-1 if np.issubdtype(sound.dtype, np.signedinteger) else 1),
        n_channels=sound.n_channels,
        wait=wait if not isinstance(wait, bool) else sound.duration,
        **kwargs
    )
