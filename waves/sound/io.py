"""Interface that add reading capabilities to Sound types."""
import numbers
import struct
import wave

import numpy as np

import pysndfile as snd


class SoundIO:
    """Adds class methods for sound instance creations from files or data
    and properties for data retrieval.
    
    By design, only supports ``.wav`` files. Reading methods return a
    :py:class:`breaks.sound.sound.Sound` if the sample has more than 1 channel,
    otherwise returns a :py:class:`breaks.sound.mono.MonoSound`.
    """
    
    # ------------------ INTERNAL --------------------
    
    def _init_f(self):
        if not self.f:
            self.f = snd.PySndfile(filename, "r")
        else:
            self.f.seek(0, mode="r")
    
    @classmethod
    def from_sndbuffer(cls, f):
        from waves.sound.main import Sound
            
        encoding = f.encoding_str()
        if encoding.startswith("pcm"):
            bits = encoding.replace("pcm", "").replace("24", "32").replace("u8", "64")
            dtype = getattr(np, f"int{bits}")
            n_bytes = int(int(bits) / 4)
        elif encoding.startswith("float"):
            dtype = getattr(np, encoding)
            n_bytes = int(int(encoding.replace("float", "")) / 4)
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
    
    @classmethod
    def from_file(cls, filename):
        return cls.from_sndbuffer(snd.PySndfile(filename, "r"))

    # ------------------ GETTERS -------------------
    
    @property
    def data(self):
        """Returns the data array of the sound."""
        if not self.time_to_frame:
            self._init_f()
            data = self.f.read_frames(nframes=self.n_frames, dtype=self.dtype)
            self.f.seek(0, mode="r")
            return data
        else:
            return np.array(list(self.time_to_frame(t) for t in self.time_sequence))
    
    
    
    
    
    
    
    
    
    
    ######################## DEPRECATED #############################
    
    
    
    # ------------------ GETTERS -------------------
    
    @property
    def _data(self):
        """Returns the data array of the sound."""
        if not self.time_to_frame:
            self._init_f()

            hexdata = self.f.readframes()
            self.f.setpos(0)
            data = np.frombuffer(hexdata, getattr(np, f"int{self.n_bytes ** 4}"))
            
            if hasattr(self, "n_channels") and self.n_channels > 1:
                data.shape = (-1, self.n_channels)
                data = data.T
            return data
        else:
            return np.array(list(self.time_to_frame(t) for t in self.time_sequence))

    @property
    def dataframes(self):
        """Returns each frame of the sound in a Numpy array with shape
        ``(n_frames, n_channels)``.
        """
        return self.data.T
    
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
    def _from_file(cls, filename, n_frames=-1):
        """Opens a sound from a file.
        
        Parameters
        ----------
        
        filename : str
          File path in the disk to open.
        
        n_frames : int, optional
          Number of frames to read from the file. By default, the whole file is read.
          
        Examples
        --------
        
        >>> Sound.from_file("stereo.wav")
        <waves.sound.stereo.StereoSound object at ...>
        
        >>> Sound.from_file("mono.wav")
        <waves.sound.mono.MonoSound object at ...>
        """
        with wave.open(filename, "rb") as f:
            obj = cls.from_buffer(f, n_frames=n_frames, filename=filename)
        return obj

    @classmethod
    def from_buffer(cls, f, n_frames=-1, filename=None):
        """Opens a sound from a :py:class:`wave.Wave_read` buffer.
        
        The buffer is not closed nor seeked after the read, so this is your responsability
        if you want to preserve your memory space or keep reading from the file after this
        method returns.
        
        Parameters
        ----------
        
        f : :py:class:`wave.Wave_read`
          File buffer to read. Must be opened with ``wave.open("<filename>", "rb")``.
        
        n_frames : int, optional
          Number of frames to read from the buffer. By default, the whole buffer is read.
        
        Examples
        --------
        
        >>> import wave
        >>> with wave.open("stereo.wav", "rb") as f:
        ...     sound = Sound.from_buffer(f)
        >>> sound
        <waves.sound.stereo.StereoSound object at ...>
        
        >>> with wave.open("mono.wav", "rb") as f:
        ...     sound = Sound.from_buffer(f)
        >>> sound
        <waves.sound.mono.MonoSound object at ...>
        """
        from waves.sound.mono import MonoSound

        n_bytes = f.getsampwidth()
        n_channels = f.getnchannels()
        n_frames = f.getnframes()
        fps = f.getframerate()
        
        if not filename:
            filename = f._file.file.name

        if n_channels == 1:
            return MonoSound(
                n_frames=n_frames,
                n_bytes=n_bytes,
                fps=fps,
                filename=filename,
            )
        
        from waves.sound.stereo import StereoSound

        return StereoSound(
            [
                MonoSound(
                    n_frames=n_frames,
                    n_bytes=n_bytes,
                    fps=fps,
                ) for i in range(n_channels)
            ],
            filename=filename,
        )
    
    @classmethod
    def from_datatimes(cls, frame_time_to_data, n_bytes=2, **kwargs):
        """Build a sound object reading from frames arrays data, one array data by frame
        given a time.
        
        Parameters
        ----------
        
        frame_time_to_data : function
          Function that takes an argument which refers to the time of the frame and
          returns the numerical data for that frame. The returned value must be a
          subscriptable object with the data for the frame at given time for each
          channel.
        """
        from waves.sound.mono import MonoSound
        
        # get first timeframe to get sound data
        first_frame = frame_time_to_data(0)
        if isinstance(first_frame, numbers.Number):
            n_channels = 1
        else:
            n_channels = len(first_frame)
        
        print(type(first_frame))
    
        if n_channels == 1:
            return MonoSound(
                n_bytes=n_bytes,
                time_to_frame=frame_time_to_data,
                **kwargs
            )
        
        from waves.sound.stereo import StereoSound
        
        def build_time_to_frame_function(i):
            return lambda t: frame_time_to_data(t)[i]
        
        return StereoSound([
            MonoSound(
                n_bytes=first_frame[0].nbytes,
                time_to_frame=build_time_to_frame_function(i),
                **kwargs,
            ) for i in range(n_channels)
        ])
    
    @classmethod
    def from_dataframes(cls, frame_index_to_data, n_frames, fps=44100, **kwargs):
        """Build a sound object reading from frames arrays data, one array data by frame
        index.
        
        Parameters
        ----------
        
        frame_index_to_data : function
          Function that takes an argument ``frame_index``, which refers to the index
          of the frame starting at 0 and returns the numerical data for that frame.
          The returned value must be a subscriptable object with the data for the
          frame for each channel.
        
        n_frames : int
          Total number of frames to build.
        
        fps : int, optional
          Number of frames per second of the resulting sound.
        
        Examples
        --------
        
        >>> # mono
        >>> f = wave.open("mono.wav", "rb")
        >>> n_frames, n_bytes = (f.getnframes(), f.getsampwidth())
        >>> hexdata = f.readframes(n_frames)
        >>> data = np.frombuffer(hexdata, getattr(np, f"int{n_bytes ** 4}"))
        >>> Sound.from_dataframes(lambda i: data[i], n_frames, f.getframerate())
        <waves.sound.mono.MonoSound object at ...>
        >>> f.close()
        
        >>> # stereo
        >>> f = wave.open("stereo.wav", "rb")
        >>> n_frames, n_bytes = (f.getnframes(), f.getsampwidth())
        >>> hexdata = f.readframes(-1)
        >>> data = np.frombuffer(hexdata, getattr(np, f"int{n_bytes ** 4}"))
        >>> data.shape = (-1, f.getnchannels())
        >>> Sound.from_dataframes(lambda i: data[i], n_frames, f.getframerate())
        <waves.sound.stereo.StereoSound object at ...>
        >>> f.close()
        """
        from waves.sound.mono import MonoSound
        
        # get first timeframe to get sound data
        first_frame = frame_index_to_data(0)

        if isinstance(first_frame, numbers.Number):
            n_channels = 1
            n_bytes = first_frame.nbytes
        else:
            n_channels = len(first_frame)
            n_bytes = first_frame[0].nbytes

        if n_channels == 1:
            return MonoSound(
                n_frames=n_frames,
                fps=fps,
                n_bytes=n_bytes,
                time_to_frame=lambda t: frame_index_to_data(int(t * fps)),
                **kwargs
            )
        
        from waves.sound.stereo import StereoSound
        
        def build_time_to_frame_function(i):
            return lambda t: frame_index_to_data(int(t * fps))[i]
        
        return StereoSound([
            MonoSound(
                n_bytes=n_bytes,
                time_to_frame=build_time_to_frame_function(i)
            ) for i in range(n_channels)
        ])
    
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
