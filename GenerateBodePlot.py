# Creates a Bode plot from a given set of frequencies,
# magnitudes, and phases
# Date: December 21, 2021
# Author: Jianan Zhao and Stewart Pearson

def GenerateBodePlot(freqs, dB, phase)
    fig, ax1 = plt.subplots()
    plt.grid(True)

    color = 'tab:red'
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('Magnitude [dB]', color=color)
    ax1.set_xscale('log')
    ax1.plot(freqs, dB, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Phase [deg]', color=color)  # we already handled the x-label with ax1
    ax2.plot(freqs, phase, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    return 0