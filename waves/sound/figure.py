"""Plottable sounds interface."""
import matplotlib.pyplot as plt
import numpy as np


def figure(sound, title="Sound data"):
    fig, axes = plt.subplots(sound.n_channels)
    if not isinstance(axes, np.ndarray):
        # for mono, axes is a `matplotlib.axes._subplots.AxesSubplot` object
        axes = np.array([axes])
        _need_label = False
    else:
        _need_label = True
    fig.suptitle(title)

    data = [sound.data] if sound.n_channels == 1 else sound.data

    for i in range(sound.n_channels):
        time_sequence = list(sound.time_sequence)

        color = "tab:red" if i % 2 else "tab:blue"
        label = ("L" if i % 2 == 0 else "R") + str(round((i + 1.1) / 2))
        axes[i].plot(
            time_sequence,
            data[i],
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
                fontweight="bold",
            )
        axes[i].set_xlim(0, time_sequence[-1])
        axes[i].set_xticks(
            np.arange(0, time_sequence[-1], round(sound.duration / 15, 1))
        )

    return (fig, axes)
