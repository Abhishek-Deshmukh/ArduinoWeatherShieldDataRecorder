import numpy as np
import matplotlib.pyplot as plt

class Plot:
    def __init__(self, size):
        self.lines = []
        self.axes = []
        self.size = size

    def update_plot(self, y_vecs):
        # cleaning input
        if len(y_vecs[0]) > self.size:
            y_vecs = y_vecs[0:4, -self.size:]
        else:
            x_vec = np.arange(0, self.size)
            y = np.zeros((4, self.size))
            y[0:4, self.size - len(y_vecs[0]) :] = y_vecs
            y_vecs = y
        # only the first time make plots
        if self.lines == []:
            self.lines = [[], [], [], []]
            self.axes = []
            plt.ion()
            fig = plt.figure(num="Weather station output")
            labels = ["Humidity (%)", "Temperature (F)", "Pressure (Pa)", "Light (V)"]
            for i in range(4):
                self.axes.append(fig.add_subplot(221 + i))
                (self.lines[i],) = self.axes[-1].plot(x_vec, y_vecs[i], "-o", alpha=0.8)
                self.axes[-1].set_ylabel(labels[i])
                self.axes[-1].set_xlabel("Time (s)")
                self.axes[-1].grid()
        else: # then just update the data
            for i in range(4):
                ar_max, ar_min = max(y_vecs[i]), min(y_vecs[i])
                pad = 0.2 * (ar_max - ar_min)
                self.lines[i].set_ydata(y_vecs[i])
                self.axes[i].set_ylim([ar_min - pad, ar_max + pad])
            plt.pause(0.1)