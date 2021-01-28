Quickstart
==========

***********************
Open a file and play it
***********************

.. code-block::

   from waves import Sound

   sound = Sound.from_file("stereo.wav")
   sound.play()

**********************************
Open a file and see their waveform
**********************************

.. code-block::

   from waves import Sound

   sound = Sound.from_file("stereo.wav")
   sound.plot()


****************************
Viewing and playing together
****************************

.. code-block::

   from waves import Sound

   sound = Sound.from_file("stereo.wav")
   sound.play(wait=False)
   sound.plot()
