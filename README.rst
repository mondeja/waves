waves
=====

.. image:: https://img.shields.io/pypi/v/waves?logo=pypi&logoColor=white
   :target: https://pypi.org/project/waves/
   :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/waves?logo=python&logoColor=white
   :target: https://pypi.org/project/waves/
   :alt: Python versions
.. image:: https://img.shields.io/github/workflow/status/mondeja/waves/Github%20Pages?label=docs&logo=github
   :target: https://mondeja.github.io/waves/
   :alt: Github Pages

.. image:: https://img.shields.io/github/workflow/status/mondeja/waves/CI?logo=github
   :target: https://github.com/mondeja/waves/actions?query=workflow%3A%22CI%22
   :alt: Build status on Github Actions
.. image:: https://img.shields.io/coveralls/github/mondeja/waves/master?logo=coveralls
   :target: https://coveralls.io/github/mondeja/waves?branch=master
   :alt: Code coverage from coveralls.io


Utility to work with WAV files in a simple way.

It's built on top of pysndfile_ (a Cython wrapper for libsndfile_) and
shouldn't be confused with the builtin library wave_.

Installation
~~~~~~~~~~~~

.. code-block::

   pip install waves

You can pass the following extras to the installation:

* ``play``: you will can listen the sound using ``sound.play`` using pygame.
* ``plot``: you will can paint the spectrum of sounds as figures in matplotlib canvas using ``sound.plot``.

.. code-block::

    pip install waves[play,plot]

Documentation_
~~~~~~~~~~~~~~

.. _pysndfile: https://pysndfile.readthedocs.io/en/latest/LONG_DESCR.html
.. _libsndfile: http://www.mega-nerd.com/libsndfile/
.. _wave: https://docs.python.org/3/library/wave.html
.. _Documentation: https://mondeja.github.io/waves
