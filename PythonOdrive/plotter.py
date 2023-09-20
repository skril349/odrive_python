import matplotlib.pyplot as plt

def update_plot(timestamps, positions, intensities, voltages, torques, ax1, ax2, ax3, ax4):
    ax1.clear()
    ax1.plot(timestamps, positions, label='Position')
    ax1.set_ylabel('Position')
    ax1.legend()

    ax2.clear()
    ax2.plot(timestamps, intensities, label='Intensity')
    ax2.set_ylabel('Intensity')
    ax2.legend()

    ax3.clear()
    ax3.plot(timestamps, voltages, label='Voltage')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Voltage')
    ax3.legend()

    ax4.clear()
    ax4.plot(timestamps, torques, label='Torque')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Torque (N.cm)')
    ax4.legend()

    plt.pause(0.01)
