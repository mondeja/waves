"""Plottable sounds interface."""
import matplotlib.pyplot as plt
import numpy as np


class PlottableSound:
    def figure(self, title="Sound data"):
        """Returns a matplotlib figure with channels plotted.
        
        Parameters
        ----------
        
        title : str, optional
          Figure title.
        """
        channels = [self] if not hasattr(self, "channels") else self.channels

        fig, axes = plt.subplots(len(channels))
        if not isinstance(axes, np.ndarray):
            # for mono, axes is a `matplotlib.axes._subplots.AxesSubplot` object
            axes = np.array([axes])
            _need_label = False
        else:
            _need_label = True
        fig.suptitle(title)

        for i, channel in enumerate(channels):
            color = "tab:red" if i % 2 else "tab:blue"
            label = ("L" if i % 2 == 0 else "R") + str(round((i + 1.1) / 2))
            axes[i].plot(
                channel.time_sequence,
                channel.data,
                color=color,
                linewidth=0.3,
            )
            if _need_label:
                axes[i].set_ylabel(
                    label,
                    labelpad=-7,
                    rotation=0,
                    va="center",
                    color=color,
                    fontweight="bold"
                )
            axes[i].set_xlim(0, channel.time_sequence[-1])
            axes[i].set_xticks(
                np.arange(
                    0,
                    channel.time_sequence[-1],
                    round(channel.duration / 15, 1)
                )
            )

        return (fig, axes)
    
    def plot(self, show=True, **kwargs):
        """Plots the figure that represents the sound using matplotlib.
        
        show : bool, optional
          Shows the figure using ``plt.show``.
        """
        fig, axs = self.figure(**kwargs)
        if show:
            plt.show()