import matplotlib.pyplot as plt

def update_plot(timestamps, positions, intensities, voltages, torques, ax1, ax2, ax3, ax4):
    ax1.clear()
    ax1.plot(timestamps, positions, label='Position (turns)')
    ax1.set_ylabel('Position (turns)')
    ax1.legend()

    ax2.clear()
    ax2.plot(timestamps, intensities, label='Intensity (A)')
    ax2.set_ylabel('Intensity (A)')
    ax2.legend()

    ax3.clear()
    ax3.plot(timestamps, voltages, label='Voltage (V)')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Voltage (V)')
    ax3.legend()

    ax4.clear()
    ax4.plot(timestamps, torques, label='Torque (N·cm)')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Torque (N.cm)')
    ax4.legend()

    plt.pause(0.01)
