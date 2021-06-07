"""Interface that add reading capabilities to Sound types."""
import numbers
import os

import numpy as np
import pysndfile as snd


class SoundIO:
    """Adds class methods for sound instance creations from files or data
    and properties for data retrieval.
    """

    # ------------------ INTERNAL --------------------

    def _init_f(self):
        if not self.f:
            self.f = snd.PySndfile(self.filename, "r")
        else:
            self.f.seek(0, mode="r")

    def _read_frames(self):
        self._init_f()
        data = self.f.read_frames(nframes=self.n_frames, dtype=self.dtype)
        self.f.seek(0, mode="r")
        return data

    # ------------------ OPENERS --------------------

    @classmethod
    def from_file(cls, filename):
        """Open a sound from a file.

        Parameters
        ----------

        filename : str
          File path in the disk to open.

        Returns
        -------

        :py:class:`waves.Sound`
          :py:class:`waves.Sound` instance.

        Raises
        ------

        FileNotFoundError
          If the file does not exists in the provided path.
        IsADirectoryError
          If the provided path points to a directory.

        Examples
        --------

        >>> from waves import Sound
        >>>
        >>> Sound.from_file("tests/files/stereo.wav")
        <waves.sound.main.Sound object at ...>
        >>>
        >>> Sound.from_file("tests/files/mono.wav")
        <waves.sound.main.Sound object at ...>
        """
        try:
            return cls.from_sndbuffer(snd.PySndfile(filename, "r"))
        except OSError as err:
            if "No such file or directory" in str(err):
                if os.path.isdir(filename):
                    raise IsADirectoryError(f"'{filename}' is a directory") from None
                raise FileNotFoundError(f"'{filename}' file not found") from None
            raise err

    @classmethod
    def from_sndbuffer(cls, f):
        """Open a sound file from a :py:class:`pysndfile.PySndfile` instance.

        Parameters
        ----------

        f : :py:class:`pysndfile.PySndfile`
          Opened instance of wrapper reading and writing class of pysndfile.

        Returns
        -------

        :py:class:`waves.Sound`
          :py:class:`waves.Sound` instance.

        Examples
        --------

        >>> import pysndfile as snd
        >>> from waves import Sound
        >>>
        >>> Sound.from_sndbuffer(snd.PySndfile("tests/files/stereo.wav", "r"))
        <waves.sound.main.Sound object at ...>
        >>>
        >>> Sound.from_sndbuffer(snd.PySndfile("tests/files/mono.wav", "r"))
        <waves.sound.main.Sound object at ...>
        """
        from waves.sound.main import Sound

        encoding = f.encoding_str()
        if encoding.startswith("pcm"):
            bits = encoding.replace("pcm", "").replace("24", "32").replace("u8", "64")
            dtype = getattr(np, f"int{bits}")
            n_bytes = int(int(bits) >> 3)
        elif encoding.startswith("float"):
            dtype = getattr(np, encoding)
            n_bytes = int(int(encoding.replace("float", "")) >> 3)
        else:
            dtype = np.float64
            n_bytes = 8

        n_channels, fps, n_frames = (f.channels(), f.samplerate(), f.frames())
        filename, metadata = (f.get_name(), f.get_strings())

        return Sound(
            n_frames=n_frames,
            n_bytes=n_bytes,
            n_channels=n_channels,
            fps=fps,
            dtype=dtype,
            filename=filename,
            f=f,
            metadata=metadata,
        )

    # ------------------ GENERATORS --------------------

    @classmethod
    def from_dataframes(cls, index_to_frame, fps=44100, **kwargs):
        """Build a sound object reading from frames arrays data, one array of data
        by frame index.

        Parameters
        ----------

        index_to_frame : function
          Function that takes an argument ``i``, which refers to the index of the
          frame starting at 0 and returns the numerical data for that frame. The
          returned value must be a subscriptable object with the data for the frame
          for each channel.

        fps : int, optional
          Number of frames per second of the resulting sound.

        Examples
        --------

        >>> # mono from file
        >>> import wave
        >>> import numpy as np
        >>> from waves import Sound
        >>>
        >>> f = wave.open("tests/files/mono.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> data = np.frombuffer(hexdata, getattr(np, f"int{f.getsampwidth() << 3}"))
        >>>
        >>> def index_to_frame(i):
        ...     try:
        ...         return data[i]
        ...     except IndexError:
        ...         raise StopIteration
        >>>
        >>> Sound.from_dataframes(index_to_frame, f.getframerate())
        <waves.sound.main.Sound object at ...>
        >>> f.close()

        >>> # mono from generated data
        >>> import numpy as np
        >>> from waves import Sound
        >>>
        >>> duration, fps, frequency, volume = (3, 44100, 110, 0.5)
        >>> t = np.linspace(0., duration, duration * fps)
        >>> amplitude = np.iinfo(np.int16).max * volume
        >>> data = (amplitude * np.sin(frequency * 2. * np.pi * t)).astype(np.int16)
        >>> Sound.from_dataframes(lambda i: data[i], fps=fps)
        <waves.sound.main.Sound object at ...>

        >>> # stereo from file
        >>> import wave
        >>> import numpy as np
        >>> from waves import Sound
        >>>
        >>> f = wave.open("tests/files/stereo.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> data = np.frombuffer(hexdata, getattr(np, f"int{f.getsampwidth() << 3}"))
        >>> data.shape = (-1, f.getnchannels())
        >>>
        >>> def index_to_frame(i):
        ...     try:
        ...         return data[i]
        ...     except IndexError:
        ...         raise StopIteration
        >>>
        >>> Sound.from_dataframes(index_to_frame, f.getframerate())
        <waves.sound.main.Sound object at ...>
        >>> f.close()

        >>> # stereo from generated data
        >>> import numpy as np
        >>> from waves import Sound
        >>>
        >>> duration, fps, frequencies, volume = (3, 44100, (110, 440), 0.4)
        >>> t = np.linspace(0., duration, duration * fps)
        >>> amplitude = np.iinfo(np.int16).max * volume
        >>> data_left = (
        ...     amplitude * np.sin(frequencies[0] * 2. * np.pi * t)
        ... ).astype(np.int16)
        >>> data_right = (
        ...     amplitude * np.sin(frequencies[1] * 2. * np.pi * t)
        ... ).astype(np.int16)
        >>> Sound.from_dataframes(
        ...     lambda i: np.array([data_left[i], data_right[i]]), fps=fps
        ... )
        <waves.sound.main.Sound object at ...>
        """
        return cls.from_datatimes(
            lambda t: index_to_frame(int(round(t * fps))), fps=fps, **kwargs
        )

    @classmethod
    def from_datatimes(cls, time_to_frame, fps=44100, **kwargs):
        """Build a sound object reading from frames arrays data, one array data by
        frame given a time.

        Parameters
        ----------

        time_to_frame : function
          Function that takes an argument ``t`` which refers to the second of the
          frame and returns the numerical data for that frame. The returned value
          must be a subscriptable object with the data for the frame at given time
          for each channel.

        fps : int, optional
          Number of frames per second of the resulting sound.

        Examples
        --------

        >>> # mono generating sine wave
        >>> import numpy as np
        >>> from waves import Sound
        >>>
        >>> duration, fps, frequency, volume = (3, 44100, 110, 0.5)
        >>> amplitude = np.iinfo(np.int16).max * volume
        >>>
        >>> def time_to_frame(t):
        ...     return (np.sin(frequency * 2 * np.pi * t) * amplitude).astype(
        ...         np.int16
        ...     )
        >>>
        >>> Sound.from_datatimes(time_to_frame, fps=fps).with_duration(duration)
        <waves.sound.main.Sound object at ...>

        >>> # stereo generating sine waves
        >>> import numpy as np
        >>> from waves import Sound
        >>>
        >>> duration, fps, frequencies, volume = (3, 44100, (110, 440), 0.5)
        >>> amplitude = np.iinfo(np.int16).max * volume
        >>>
        >>> def time_to_frame(t):
        ...     return [
        ...         (np.sin(frequencies[0] * 2 * np.pi * t) * amplitude).astype(
        ...             np.int16
        ...         ),
        ...         (np.sin(frequencies[1] * 2 * np.pi * t) * amplitude).astype(
        ...             np.int16
        ...         ),
        ...     ]
        >>>
        >>> Sound.from_datatimes(time_to_frame, fps=fps).with_duration(duration)
        <waves.sound.main.Sound object at ...>
        """
        from waves.sound.main import Sound

        # get first timeframe to get sound data
        first_frame = time_to_frame(0)

        if isinstance(first_frame, numbers.Number):
            n_channels = 1
            n_bytes = first_frame.nbytes
            dtype = type(first_frame)
        else:
            n_channels = len(first_frame)
            n_bytes = first_frame[0].nbytes
            dtype = type(first_frame[0])

        return Sound(
            n_bytes=n_bytes,
            n_channels=n_channels,
            fps=fps,
            dtype=dtype,
            time_to_frame=time_to_frame,
            **kwargs,
        )

    @classmethod
    def from_byteframes(cls, index_to_hexframe, fps=44100, **kwargs):
        """Build a sound object reading from frames bytes, one hex data chunk by frame
        index.

        Parameters
        ----------

        index_to_hexframe : function
          Function that takes an argument ``i``, which refers to the index of the
          frame starting at 0 and returns the bytes object for that frame. The
          returned value must be a subscriptable object with the bytes for the frame
          for each channel.

        fps : int, optional
          Number of frames per second of the resulting sound.

        Examples
        --------

        >>> # mono from file
        >>> import wave, struct
        >>> from waves import Sound
        >>>
        >>> f = wave.open("tests/files/mono.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> hexframes = []
        >>> for bytes_frame in struct.iter_unpack(f"{f.getsampwidth()}c", hexdata):
        ...     hexframes.append(b"".join(bytes_frame))
        >>>
        >>> def index_to_hexframe(i):
        ...     try:
        ...         return hexframes[i]
        ...     except IndexError:
        ...         raise StopIteration
        >>>
        >>> Sound.from_byteframes(index_to_hexframe, fps=f.getframerate())
        <waves.sound.main.Sound object at ...>
        >>> f.close()

        >>> # stereo from file
        >>> import wave, struct
        >>> from waves import Sound
        >>>
        >>> f = wave.open("tests/files/stereo.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> n_channels, n_bytes = (f.getnchannels(), f.getsampwidth())
        >>>
        >>> hexframes = []
        >>> for bytes_frame in struct.iter_unpack(f"{n_bytes * n_channels}c", hexdata):
        ...     hexframe = []
        ...     for channel_index in range(n_channels):
        ...         start = channel_index * n_bytes
        ...         end = start + n_bytes
        ...         hexframe.append(b"".join(bytes_frame[start: end]))
        ...     hexframes.append(hexframe)
        >>>
        >>> def index_to_hexframe(i):
        ...     try:
        ...         return hexframes[i]
        ...     except IndexError:
        ...         raise StopIteration
        >>>
        >>> Sound.from_byteframes(index_to_hexframe, fps=f.getframerate())
        <waves.sound.main.Sound object at ...>
        >>> f.close()
        """
        from waves.sound.main import Sound

        # get first frame so we can retrieve number of bytes and channels
        hexdata = index_to_hexframe(0)
        if isinstance(hexdata, bytes):
            # mono
            n_channels = 1
            n_bytes = len(hexdata)
        else:
            # stereo
            n_channels = len(hexdata)
            n_bytes = len(hexdata[0])
        dtype = kwargs.get("dtype", getattr(np, f"int{n_bytes << 3}"))

        if n_channels == 1:
            return Sound(
                fps=fps,
                n_bytes=n_bytes,
                n_channels=n_channels,
                time_to_frame=lambda t: np.frombuffer(
                    index_to_hexframe(int(round(t * fps))), dtype=dtype
                )[0],
                dtype=dtype,
                **kwargs,
            )

        def time_to_frame(t):
            frame_hexdata = index_to_hexframe(int(round(t * fps)))
            return np.array(
                [
                    np.frombuffer(frame_hexdata[0], dtype=dtype)[0],
                    np.frombuffer(frame_hexdata[1], dtype=dtype)[0],
                ]
            )

        return Sound(
            fps=fps,
            n_bytes=n_bytes,
            n_channels=n_channels,
            time_to_frame=time_to_frame,
            dtype=dtype,
            **kwargs,
        )

    @classmethod
    def from_bytetimes(cls, time_to_hexframe, fps=44100, **kwargs):
        """Build a sound object reading from frames bytes, one hex data chunk by frame
        at a time.

        Parameters
        ----------

        time_to_hexframe : function
          Function that takes an argument ``t``, which refers to the second of the
          frame starting at 0 and returns the bytes object for that frame. The
          returned value must be a subscriptable object with the bytes for the frame
          for each channel.

        fps : int, optional
          Number of frames per second of the resulting sound.

        Examples
        --------

        >>> # mono from file
        >>> import wave, struct
        >>> from waves import Sound
        >>>
        >>> f = wave.open("tests/files/mono.wav", "rb")
        >>> fps = f.getframerate()
        >>> hexdata = f.readframes(-1)
        >>> hexframes = []
        >>> for bytes_frame in struct.iter_unpack(f"{f.getsampwidth()}c", hexdata):
        ...     hexframes.append(b"".join(bytes_frame))
        >>>
        >>> Sound.from_bytetimes(lambda t: hexframes[int(round(t * fps))], fps=fps)
        <waves.sound.main.Sound object at ...>
        >>> f.close()

        >>> # stereo from file
        >>> import wave, struct
        >>> from waves import Sound
        >>>
        >>> f = wave.open("tests/files/stereo.wav", "rb")
        >>> hexdata, fps = (f.readframes(-1), f.getframerate())
        >>> n_channels, n_bytes = (f.getnchannels(), f.getsampwidth())
        >>>
        >>> hexframes = []
        >>> for bytes_frame in struct.iter_unpack(f"{n_bytes * n_channels}c", hexdata):
        ...     hexframe = []
        ...     for channel_index in range(n_channels):
        ...         start = channel_index * n_bytes
        ...         end = start + n_bytes
        ...         hexframe.append(b"".join(bytes_frame[start: end]))
        ...     hexframes.append(hexframe)
        >>> Sound.from_bytetimes(lambda t: hexframes[int(round(t * fps))], fps=fps)
        <waves.sound.main.Sound object at ...>
        >>> f.close()
        """
        from waves.sound.main import Sound

        # get first frame so we can retrieve number of bytes and channels
        hexdata = time_to_hexframe(0)
        if isinstance(hexdata, bytes):
            # mono
            n_channels = 1
            n_bytes = len(hexdata)
        else:
            # stereo
            n_channels = len(hexdata)
            n_bytes = len(hexdata[0])
        dtype = kwargs.get("dtype", getattr(np, f"int{n_bytes << 3}"))

        if n_channels == 1:
            return Sound(
                fps=fps,
                n_bytes=n_bytes,
                n_channels=n_channels,
                time_to_frame=lambda t: np.frombuffer(time_to_hexframe(t), dtype=dtype)[
                    0
                ],
                dtype=dtype,
                **kwargs,
            )

        def time_to_frame(t):
            frame_hexdata = time_to_hexframe(t)
            return np.array(
                [
                    np.frombuffer(frame_hexdata[0], dtype=dtype)[0],
                    np.frombuffer(frame_hexdata[1], dtype=dtype)[0],
                ]
            )

        return Sound(
            fps=fps,
            n_bytes=n_bytes,
            n_channels=n_channels,
            time_to_frame=time_to_frame,
            dtype=dtype,
            **kwargs,
        )

    # ------------------ GETTERS -------------------

    @property
    def data(self):
        """Returns the Numpy data array of the sound."""
        if self.time_to_frame:
            if self.n_frames is None:
                _data = np.array(list(self._time_to_frame_generator()))
                if self.n_channels > 1:
                    _data = _data.T
                return _data
            else:
                if self.n_channels == 1:
                    shape = self.n_frames
                else:
                    shape = (self.n_frames, self.n_channels)
                _data = np.empty(shape, dtype=self.dtype)
                for i, frame_data in enumerate(self._time_to_frame_generator()):
                    _data[i] = frame_data
                if self.n_channels > 1:
                    _data = _data.T
                return _data
        else:
            _data = self._read_frames()
            if self.n_channels > 1:
                _data = _data.T
            return _data

    @property
    def dataframes(self):
        """Returns each frame of the sound in a Numpy array with shape
        ``(n_frames, n_channels)`` if the sound is stereo, but if is mono returns a
        simple Numpy array with the values of the channel, one value for each frame.
        """
        if self.time_to_frame:
            if self.n_frames is None:
                return np.array(list(self._time_to_frame_generator()))
            else:
                if self.n_channels == 1:
                    shape = self.n_frames
                else:
                    shape = (self.n_frames, self.n_channels)
                _data = np.empty(shape, dtype=self.dtype)
                for i, frame_data in enumerate(self._time_to_frame_generator()):
                    try:
                        _data[i] = frame_data
                    except IndexError:
                        break
                return _data
        else:
            return self._read_frames()

    def _time_to_frame_generator(self):
        try:
            for t in self.time_sequence:
                yield self.time_to_frame(t)
        except StopIteration:
            self.n_frames = int(round(t * self.fps))  # assume end of sound

    def iter_chunks(self, buffersize=0b10000000000):  # 1024 frames
        """Generates each chunk of the sound data, being read at the moment
        of yielding.

        Parameters
        ----------

        buffersize : int, optional
          Number of frames generated at each chunk.
        """
        n_frames, frames_read = (self.n_frames, 0b0)

        # this implementation is slightly faster than create a counter `i` and compute
        # the frames read in the `RuntimeError` multipliying by `buffersize`
        try:
            while 1:
                _buffersize = buffersize
                yield self.f.read_frames(_buffersize, dtype=self.dtype)

                # bitwise sum (buffersize += buffersize)
                while _buffersize:
                    carry = frames_read & _buffersize
                    frames_read = frames_read ^ _buffersize
                    _buffersize = carry << 1
        except RuntimeError as err:
            if str(err).startswith("Ask"):
                self.f.seek(frames_read, mode="r")
                yield self.f.read_frames(n_frames - frames_read, dtype=self.dtype)
            else:
                raise err

    @property
    def iter_dataframes(self):
        """Generates each frame of the sound data.

        If the sound has beeen built using a generator function and its duration
        hasn't been set, this will produce an infinite loop.
        """
        if self.time_to_frame:
            yield from self._time_to_frame_generator()
        else:
            self._init_f()
            for chunk in self.iter_chunks():
                yield from chunk
            self.f.seek(0, mode="r")

    @property
    def iter_datatimes(self):
        """Generates each frame of the sound data, yielding a tuple with the
        time of the frame as first value and the data of the sound as second.

        If the sound has beeen built using a generator function and its duration
        hasn't been set, this will produce an infinite loop.
        """
        if self.time_to_frame:
            try:
                for t in self.time_sequence:
                    yield (t, self.time_to_frame(t))
            except StopIteration:
                self.n_frames = int(round(t * self.fps))  # assume end of sound
        else:
            self._init_f()
            t, t_fps = (0, 1 / self.fps)
            for chunk in self.iter_chunks():
                for frame in chunk:
                    yield (t, frame)
                    t += t_fps
            self.f.seek(0, mode="r")

    # ------------------ WRITERS -------------------

    def save(self, filename, buffersize=0b10000000000):
        """Saves an audio instance to a file.

        Parameters
        ----------

        filename : str
          System disk path in which the file will be saved.

        buffsize : int, optional
          Number of bytes stored in memory buffer while reading and writing.
          Only used if the filename to write has been created opening from a
          file in disk.
        """
        with snd.PySndfile(
            filename,
            "w",
            format=65536 | 2,
            channels=self.n_channels,
            samplerate=self.fps,
        ) as target_file:
            target_file.set_strings(self.metadata or {})

            if self.filename:
                for frames in self.iter_chunks(buffersize=buffersize):
                    target_file.write_frames(frames)
            else:
                target_file.write_frames(self.dataframes)
                self.filename = filename
