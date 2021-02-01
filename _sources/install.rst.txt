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

   pip install https://github.com/mondeja/waves/releases/download/v0.0.1/waves-0.0.1-py3-none-any.whl

.. note::

   For now, it's only possible to install it using the direct release link.
   The name of the project has been squatted in PyPI and I'm `waiting for their
   liberation <https://github.com/pypa/pypi-support/issues/873>`_.

.. _libsndfile: http://www.mega-nerd.com/libsndfile/
.. _official precompiled binary: http://www.mega-nerd.com/libsndfile/#Download
