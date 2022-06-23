"""
Weather Shield Dashboard
-----------------------

Just a python script which
- stores the data live into a file (name: YYYY-MM-DD.csv) with time
- shows a dashboard with a plot which shows the values of the input for the last 100 seconds

Author: Abhishek Anil Deshmukh (deshmukhabhishek369@gmail.com)
"""
import serial
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date
import pandas as pd

def get_data_store():
    return {
        "datetime": [],
        "humidity": [],
        "temperature": [],
        "pressure": [],
        "light": [],
    }


def main():
    # arduino specific params
    serial_port = "COM6"
    baud_rate = 9600
    try:  # connecting to a arduino
        ser = serial.Serial(serial_port, baud_rate)
    except Exception as e:
        print(e, "\n")
        print("="*20)
        print("One of the fllowing issues has occured:\n- Arduino is not properly connected\n- The port name is not correct\n\t- Try `python -m serial.tools.list_ports` to list all the ports")
        print("="*20)
        print("retrying in 10 seconds")
        return

    # variables to be used
    data = get_data_store()
    x_width = 100
    x_vec = np.arange(0, x_width)
    h_vec, t_vec, p_vec, l_vec = np.zeros((4, len(x_vec)))
    lines, axes = [], []
    def get_file_name():return str(datetime.now())[:-7].replace(":", "_") + ".csv"
    file_name = get_file_name()

    while True:
        # 1 line at a time
        line = ser.readline()
        line = line.decode("utf-8")

        try:  # parsing the input
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

        print(data["datetime"][0].date(), datetime.today().date())
        if data["datetime"][0].date() != datetime.today().date():
            # separating data
            old_data = {}
            for vec_name in data.keys():
                old_data[vec_name] = data[vec_name][:-1]
                data[vec_name] = [data[vec_name][-1]]
            # saving yesterdays data
            pd.DataFrame(old_data).to_csv(file_name, index=False)
            del old_data
            # saving todays data
            file_name = get_file_name()
            pd.DataFrame(data).to_csv(file_name, index=False)

        if len(data['datetime'])%10 == 0:
            try:
                pd.DataFrame(data).to_csv(file_name, index=False)
            except Exception as e:
                print(e)
                print("MAYBE: The file which is being written to seems to be opened by another application. Please close it too continue writing to file.")

        # making/updating the plots on the dashboard
        y_vecs = np.array([data["humidity"], data["temperature"], data["pressure"], data["light"]])
        lines, axes = update_plot(y_vecs, lines, axes, x_width)


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
            ar_max, ar_min = max(y_vecs[i]), min(y_vecs[i])
            pad = 0.2 * (ar_max - ar_min)
            lines[i].set_ydata(y_vecs[i])
            axes[i].set_ylim([ar_min - pad, ar_max + pad])
        plt.pause(0.1)
    return lines, axes  # To get these back later on


if __name__ == "__main__":
    main()
