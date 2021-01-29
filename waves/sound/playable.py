"""Playable sounds interface."""
import numpy as np

from waves.players.pygame import play_sound


class PlayableSound:
    """A playable sound is a sound that can be played. Classes inheriting from
    this class must implement a ``dataframes`` property which must return
    a simple Numpy array (1 dimension) for mono sound playing (``n_channels == 1``)
    or a Numpy array with shape ``(n_frames, n_channels)``.
    """
    
    def play(self, wait=True, **kwargs):
        """Plays the sound using pygame.
        
        Parameters
        ----------
        
        wait : bool or Number, optional
          Waits for the ending of the playing to return. Disable it if you want
          an asynchronous playing. Pass a number if you want to wait an exact time
          instead of the duration of the sound.
        """
        print("sound.play() -> bytes:", self.n_bytes, "| channels:", self.n_channels)
        print(self.dataframes)
        play_sound(
            self.dataframes,
            frequency=self.fps,
            size=(self.n_bytes << 3) * (-1 if np.issubdtype(self.dtype, np.signedinteger) else 1),
            n_channels=self.n_channels,
            wait=wait if not isinstance(wait, bool) else self.duration,
            **kwargs
        )