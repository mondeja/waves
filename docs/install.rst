Installation
============

This library depends on libsndfile_ to work, so you must install their headers
before:

* **Ubuntu/Debian**: ``sudo apt-get install libsndfile1-dev``
* **macOS/Homebrew**: ``brew install libsndfile``
* **Arch Linux**: ``sudo pacman -S libsndfile``
* **Fedora**: ``sudo dnf install libsndfile-devel``
* **Windows**: Download and install an `official precompiled binary`_.

After that, you only need to install using PIP as usually:

.. code-block:: bash

   pip install waves

You can pass the following extras to the installation:

* ``play``: you will can listen the sound using ``sound.play`` using pygame.
* ``plot``: you will can paint the spectrum of sounds as figures in matplotlib canvas using ``sound.plot``.

.. code-block::

    pip install waves[play,plot]

.. _libsndfile: http://www.mega-nerd.com/libsndfile/
.. _official precompiled binary: http://www.mega-nerd.com/libsndfile/#Download
