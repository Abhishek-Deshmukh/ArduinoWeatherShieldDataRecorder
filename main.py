import serial
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date
import pandas as pd


def main():
    # arduino specific params
    serial_port = "COM6"
    baud_rate = 9600
    ser = serial.Serial(serial_port, baud_rate)

    data = {
        "datetime": [],
        "humidity": [],
        "temperature": [],
        "pressure": [],
        "light": [],
    }
    x_width = 100
    x_vec = np.arange(0, x_width)
    h_vec, t_vec, p_vec, l_vec = np.zeros((4, len(x_vec)))
    lines, axes = [], []

    while True:
        line = ser.readline()
        line = line.decode("utf-8")

        try:
            params = line.split(", ")[:-1]
            params = list(map(lambda x: x.split(" = ")[-1], params))
            humidity = float(params[0][:-1])  # %
            temperature = float(params[1][:-1])  # F
            pressure = float(params[2][:-2])  # Pa
            light = float(params[4][:-1])  # V
        except Exception as e:
            print(
                "Couldn't parse, trying again with next data point (If this happens more than 5 times in a row, something in wrong!!!)"
            )
            continue

        data["datetime"].append(datetime.now())
        data["humidity"].append(humidity)
        data["temperature"].append(temperature)
        data["pressure"].append(pressure)
        data["light"].append(light)

        # saving to the dated file every 10 seconds
        if len(data["humidity"]) % 10 == 0:
            pd.DataFrame(data).to_csv(str(date.today()) + ".csv", index=False)

        if len(data["humidity"]) > 0:
            lines, axes = update_plot(
                np.array([
                    data["humidity"],
                    data["temperature"],
                    data["pressure"],
                    data["light"],
                ]),
                lines,
                axes,
                x_width,
            )


def update_plot(y_vecs, lines, axes, size):
    # cleaning input
    if len(y_vecs[0]) > size:
        y_vecs = y_vecs[0:4, -size:]
    else:
        x_vec = np.arange(0, size)
        y = np.zeros((4, size))
        y[0:4, size - len(y_vecs[0]) :] = y_vecs
        y_vecs = y
    # only the first time make plots
    if lines == []:
        lines = [[], [], [], []]
        axes = []
        plt.ion()
        fig = plt.figure(num="Weather station output")
        labels = ["Humidity (%)", "Temperature (F)", "Pressure (Pa)", "Light (V)"]
        for i in range(4):
            axes.append(fig.add_subplot(221 + i))
            (lines[i],) = axes[-1].plot(x_vec, y_vecs[i], "-o", alpha=0.8)
            axes[-1].set_ylabel(labels[i])
            axes[-1].set_xlabel("Time (s)")
            axes[-1].grid()
    else: # then just update the data
        for i in range(4):
            lines[i], axes[i] = set_y(lines[i], axes[i], y_vecs[i])
        plt.pause(0.1)
    return lines, axes  # To get these back later on


def set_y(line, ax, arr):
    ar_max = max(arr)
    ar_min = min(arr)
    pad = 0.2 * (ar_max - ar_min)
    line.set_ydata(arr)
    ax.set_ylim([ar_min - pad, ar_max + pad])
    return line, ax


if __name__ == "__main__":
    main()
