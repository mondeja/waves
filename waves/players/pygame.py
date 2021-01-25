"""Pygame sound playing utilities."""

import os
import time


# hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def play_sound(data, frequency=44100, size=-16, channels=2, wait=True, **kwargs):
    """Plays sound using Pygame.
    
    Parameters
    ----------
    
    data : np.ndarray
      Data array of the sound to play.
    
    frequency : int
      Number of frames per second. 
    """
    from pygame import mixer

    mixer.quit()
    mixer.init(frequency=frequency, size=size, channels=channels)

    pg_sound = mixer.Sound(array=data)
    pg_sound.play(**kwargs)
    
    if wait:
        time.sleep(wait)