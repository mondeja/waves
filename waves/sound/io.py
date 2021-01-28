"""Interface that add reading capabilities to Sound types."""
import numbers
import os
import struct
import wave

import numpy as np

import pysndfile as snd


class SoundIO:
    """Adds class methods for sound instance creations from files or data
    and properties for data retrieval.
    """
    
    # ------------------ INTERNAL --------------------
    
    def _init_f(self):
        if not self.f:
            self.f = snd.PySndfile(filename, "r")
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
        
        >>> Sound.from_file("stereo.wav")
        <waves.sound.main.Sound object at ...>
        
        >>> Sound.from_file("mono.wav")
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
        >>> from_sndbuffer(snd.PySndfile("stereo.wav", "r"))
        <waves.sound.main.Sound object at ...>
        >>> from_sndbuffer(snd.PySndfile("mono.wav", "rw"))
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
    def from_dataframes(cls, index_to_frame, fps=44100, metadata={}, **kwargs):
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
        
        metadata : dict, optional
          Meatadata for the sound, which will be included when saving it.
        
        Examples
        --------
        
        >>> # mono from file
        >>> import wave
        >>> import numpy a np
        >>> f = wave.open("mono.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> data = np.frombuffer(hexdata, getattr(np, f"int{f.getsampwidth() << 3}"))
        >>> Sound.from_dataframes(lambda i: data[i], f.getframerate())
        <waves.sound.main.Sound object at ...>
        >>> f.close()
        
        >>> # mono from generated data
        >>> import numpy as np
        >>> duration, fps, frequency, volume = (3, 44100, 110, 0.5)
        >>> t = np.linspace(0., duration, duration * fps)
        >>> amplitude = np.iinfo(np.int16).max * volume
        >>> data = (amplitude * np.sin(frequency * 2. * np.pi * t)).astype(np.int16)
        >>> Sound.from_dataframes(lambda i: data[i], fps=fps)
        <waves.sound.main.Sound object at ...>

        >>> # stereo from file
        >>> import wave
        >>> import numpy as np
        >>> f = wave.open("stereo.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> data = np.frombuffer(hexdata, getattr(np, f"int{f.getsampwidth() << 3}"))
        >>> data.shape = (-1, f.getnchannels())
        >>> Sound.from_dataframes(lambda i: data[i], f.getframerate())
        <waves.sound.main.Sound object at ...>
        >>> f.close()
        
        >>> # stereo from generated data
        >>> import numpy as np
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
    def from_datatimes(cls, time_to_frame, fps=44100, metadata={}, **kwargs):
        """Build a sound object reading from frames arrays data, one array data by frame
        given a time.
        
        Parameters
        ----------
        
        time_to_frame : function
          Function that takes an argument ``t`` which refers to the time of the frame
          and returns the numerical data for that frame. The returned value must be a
          subscriptable object with the data for the frame at given time for each
          channel.
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
            metadata=metadata,
            **kwargs
        )

    # ------------------ GETTERS -------------------

    @property
    def data(self):
        """Returns the Numpy data array of the sound."""
        if not self.time_to_frame:
            data = self._read_frames()
            if self.n_channels > 1:
                data = data.T
            return data
        else:
            data = []
            for i, t in enumerate(self.time_sequence):
                try:
                    data.append(self.time_to_frame(t))
                except IndexError:
                    self.n_frames = i  # assume end of sound
                    break
            return np.array(data).T
    
    @property
    def dataframes(self):
        """Returns each frame of the sound in a Numpy array with shape
        ``(n_frames, n_channels)`` if the sound is stereo, but if is mono returns a
        simple Numpy array with the values of the channel, one value for each frame.
        """
        if not self.time_to_frame:
            return self._read_frames()
        else:
            data = []
            for i, t in enumerate(self.time_sequence):
                try:
                    data.append(self.time_to_frame(t))
                except IndexError:
                    self.n_frames = i  # assume end of sound
                    break
            return np.array(data)
    
    
    
    ######################## DEPRECATED #############################
    
    

    
    
    # ------------------ ITERATORS -------------------
    
    def iter_datatimes(self, duration, start=0):
        for dataframe in self.iter_dataframes(duration * self.fps,
                                              start=start * self.fps):
            yield dataframe
    
    def iter_dataframes(self, n_frames, start=0):
        numpy_datatype = getattr(np, f"int{self.n_bytes ** 4}")

        if not self.time_to_frame:
            if self.n_channels == 1:
                for bytes in self.iter_byteframes(n_frames, start=start):
                    yield np.frombuffer(bytes, numpy_datatype)
            else:
                for bytesframe in self.iter_byteframes(n_frames, start=start):
                    yield np.frombuffer(b"".join(bytesframe[0]), numpy_datatype)
        else:
            for t in self.time_sequence[start: start + n_frames]:
                yield self.time_to_frame(t)
    
    def iter_bytetimes(self, n_frames, start=0):
        for dataframe in self.iter_byteframes(duration * self.fps,
                                              start=start * self.fps):
            yield dataframe
    
    def iter_byteframes(self, n_frames, start=0):
        if not self.time_to_frame:
            self._init_f()
            
            if start:
                self.f.setpos(start)
            
            n_channels, n_bytes = (self.n_channels, self.n_bytes)
            framesize = n_channels * n_bytes
            buffersize = n_frames * framesize
            
            if n_channels == 1:
                # fast iteration for mono files
                while True:
                    bytes = self.f._data_chunk.read(buffersize)
                    if bytes == b"":
                        break
                    yield bytes
            else:
                # not so fast iteration for multiple channels
                while True:
                    bytes = self.f._data_chunk.read(buffersize)
                    if bytes == b"":
                        break
                    bytesframes = []
                    for fi in range(n_frames):
                        bytesframe = []
                        for chi in range(n_channels):
                            start = fi * framesize + (chi * n_bytes)
                            bytesframe.append(bytes[start: start + n_bytes])
                        bytesframes.append(bytesframe)                    
                    yield bytesframes

            self.f.setpos(0)
        else:
            raise IOError(
                "The data of this sound is created on the fly using the function"
                f" '{str(self.time_to_frame)}'. Please, call 'sound.iter_dataframes'"
                " instead."
            )
    
    # ------------------ WRITE methods -------------------
    
    def save(self, filename, buffsize=262144):
        """Saves an audio instance to a file.
        
        Parameters
        ----------
        
        filename : str
          System disk path in which the file will be saved.
        
        buffsize : int, optional
          Number of bytes stored in memory buffer while reading and writing.
        """
        if self.filename:
            with wave.open(self.filename, "r") as source_file, \
                    wave.open(filename, "w") as target_file:
                # set parameters for output
                target_file.setparams((
                    self.n_channels,
                    self.n_bytes,
                    self.fps,
                    self.n_frames,
                    'NONE',
                    'not compressed'
                ))
            
    # ------------------ READ methods -------------------
    
    @classmethod
    def from_byteframes(cls, frame_index_to_hexdata, n_frames, fps=44100, **kwargs):
        """Build a sound object reading from frames bytes, one hex data chunk by frame
        index.
        
        This method is slow and their recommended use is restricted to small portions
        of audio in some contexts where could be useful.
        
        Parameters
        ----------
        
        frame_index_to_hexdata : function
          Function that takes an argument ``frame_index``, which refers to the index
          of the frame starting at 0 and returns the bytes object for that frame.
          The returned value must be a subscriptable object with the bytes for the
          frame for each channel.
        
        n_frames : int
          Total number of frames to build.
        
        fps : int, optional
          Number of frames per second of the resulting sound.
        
        Examples
        --------
        
        >>> # mono
        >>>
        >>> import wave, struct
        >>> f = wave.open("mono.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> channel_hexframes = []
        >>> for bytes in struct.iter_unpack(f"{f.getsampwidth()}c", hexdata):
        ...     channel_hexframes.append(b"".join(bytes))
        >>>
        >>> Sound.from_byteframes(lambda i: [channel_hexframes[i]],
        ...                       f.getnframes(),
        ...                       f.getframerate())
        <waves.sound.mono.MonoSound object at ...>
        >>> f.close()
        
        >>> # stereo
        >>>
        >>> import wave, struct
        >>> f = wave.open("stereo.wav", "rb")
        >>> hexdata = f.readframes(-1)
        >>> n_channels = f.getnchannels()
        >>> n_bytes = f.getsampwidth()
        >>>
        >>> channels_hexframes = []
        >>> for bytes in struct.iter_unpack(f"{n_bytes * n_channels}c", hexdata):
        ...     channels_hexframe = []
        ...     for channel_index in range(n_channels):
        ...         start = channel_index * n_bytes
        ...         end = start + n_bytes
        ...         channels_hexframe.append(b"".join(bytes[start: end]))
        ...     channels_hexframes.append(channels_hexframe)
        >>>
        >>> Sound.from_byteframes(lambda i: channels_hexframes[i],
        ...                       f.getnframes(),
        ...                       f.getframerate())
        <waves.sound.mono.StereoSound object at ...>
        """
        from waves.sound.mono import MonoSound
    
        # get first frame so we can retrieve number of bytes and channels
        channels_hexdata = frame_index_to_hexdata(0)
        if isinstance(channels_hexdata[0], bytes):
            # mono
            n_channels = len(channels_hexdata)
            n_bytes = len(channels_hexdata[0])
        else:
            # stereo
            n_channels = len(channels_hexdata[0])
            n_bytes = len(channels_hexdata[0][0])

        if n_channels == 1:
            return MonoSound(
                n_frames=n_frames,
                fps=fps,
                n_bytes=n_bytes,
                time_to_frame=lambda t: int.from_bytes(
                    frame_index_to_hexdata(int(t * fps))[0], "big"
                ),
                **kwargs
            )
        
        from waves.sound.stereo import StereoSound
        
        def build_time_to_frame_function(i):
            return lambda t: int.from_bytes(
                frame_index_to_hexdata(int(t * fps))[i], "big"
            )
        
        return StereoSound([
            MonoSound(
                n_bytes=n_bytes,
                time_to_frame=build_time_to_frame_function(i)
            ) for i in range(n_channels)
        ])
    
    
    
    # TODO:
    #   - open from hex at time, one hex data frame by frame time ``from_bytetimes``
