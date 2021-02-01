"""Plottable sounds interface."""
import matplotlib.pyplot as plt

from waves.sound.figure import figure


def plot(sound, show=True, **kwargs):
    fig, axs = figure(sound, **kwargs)
    if show:
        plt.show()
