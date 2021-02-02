.. currentmodule:: waves

Sound
=====

.. class:: Sound

   Main class for all sounds.

   Its import is very simple:

   >>> from waves import Sound

   >>> import waves
   >>> waves.Sound
   <class 'waves.sound.main.Sound'>

   The class :py:class:`waves.Sound` is not intended to be built using their
   initialization method, instead must be used one of the opener or generators
   class methods.

   .. raw:: html

      <hr/>
      <h4 class="centered">OPENERS</h4>

   Openers class methods creates a :py:class:`waves.Sound` instance from a file
   in the disk or a buffer in memory:

   .. automethod:: Sound.from_file
   .. automethod:: Sound.from_sndbuffer

   .. raw:: html

      <h4 class="centered" style="padding-top: 33px;">SOUND GENERATORS</h4>

   Generator class methods creates a :py:class:`waves.Sound` instance using an
   interpolator function which build the array of values for the sound for each
   frame.

   By convenience, the next rule is follow:

   - If the sound is mono, the generator function must return one value at a
     time or frame.
   - If the sound is stereo, the generator function must return one array for
     each time or frame whose length will determine the number of channels.

   .. automethod:: Sound.from_datatimes
   .. automethod:: Sound.from_dataframes
   .. automethod:: Sound.from_bytetimes
   .. automethod:: Sound.from_byteframes

   .. raw:: html

      <hr/>
      <h4 class="centered">GETTERS</h4>

   .. autoattribute:: Sound.n_frames
      :annotation: int

   .. autoattribute:: Sound.n_bytes
      :annotation: int

   .. autoattribute:: Sound.n_channels
      :annotation: int

   .. autoattribute:: Sound.fps
      :annotation: int

   .. autoattribute:: Sound.dtype
      :annotation: type

   .. autoattribute:: Sound.filename
      :annotation: str

   .. autoattribute:: Sound.time_to_frame
      :annotation: function

   .. autoattribute:: Sound.metadata
      :annotation: dict

   .. attribute:: Sound.data
      :type: np.ndarray

      Numpy data array of the sound. If the sound is stereo, returns one Numpy
      array per channel, but if the sound is mono returns one Numpy array with
      the values of the sound for the channel.

   .. attribute:: Sound.dataframes
      :type: np.ndarray

      Numpy data array of the sound for each frame. If the sound is stereo,
      returns one Numpy array per frame, but if the sound is mono returns one
      Numpy array with the values of the sound for the channel, one array for
      each frame.

   .. autoproperty:: Sound.iter_dataframes
   .. autoproperty:: Sound.iter_datatimes
   .. autoproperty:: Sound.iter_chunks

   .. raw:: html

      <hr/>
      <h4 class="centered">WRITERS</h4>

   .. automethod:: Sound.save

   .. raw:: html

      <hr/>
      <h4 class="centered">INTERACTIVE</h4>

   .. method:: play(wait=True, **kwargs)

      Plays a sound using pygame.

      wait : bool or Number, optional
        Waits for the ending of the playing to return. Disable it if you want
        an asynchronous playing. Pass a number if you want to wait an exact time
        instead of the duration of the sound.

   .. method:: plot(show=True, **kwargs)

      Plots the figure that represents the sound using matplotlib.

      show : bool, optional
        Shows the figure using ``plt.show``.

   .. method:: figure(title="Sound data")

      Returns a basic matplotlib figure with the channels of the sound plotted.

      title : str, optional
        Figure title.
