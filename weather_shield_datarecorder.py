"""
Weather Shield Dashboard
-----------------------

Just a python script which
- stores the data live into a file (name: YYYY-MM-DD.csv) with time
- shows a dashboard with a plot which shows the values of the input for the last 100 seconds

Author: Abhishek Anil Deshmukh (deshmukhabhishek369@gmail.com)
"""
import serial
import numpy as np
from datetime import datetime, date
import pandas as pd
from live_plot import Plot
import configparser


def main():
    # arduino specific params

    config = configparser.ConfigParser()
    config.read("./config.ini")
    serial_port = config["Arduino"]["SerialPort"]
    baud_rate = int(config["Arduino"]["BaudRate"])
    try:  # connecting to a arduino
        ser = serial.Serial(serial_port, baud_rate)
    except Exception as e:
        print(e, "\n")
        print("="*20)
        print(" MAYBE:\nOne of the following issues has occured:\n- Arduino is not properly connected\n- The port name is not correct\n\t- Try `python -m serial.tools.list_ports` to list all the ports")
        print("="*20)
        return

    # variables to be used
    data = {
        "datetime": [],
        "humidity": [],
        "temperature": [],
        "pressure": [],
        "light": [],
    }
    x_width = 100
    h_vec, t_vec, p_vec, l_vec = np.zeros((4, x_width))
    def get_file_name(): return f"./{str(datetime.now())[:-7].replace(':', '_')}.csv"
    file_name = get_file_name()
    dashboard = Plot(x_width)

    while True:
        line = ser.readline().decode("utf-8")
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
                print("MAYBE: The file which is being written to seems to be opened by another application. Please close it to continue writing to file.")

        # making/updating the plots on the dashboard
        y_vecs = np.array([data["humidity"], data["temperature"], data["pressure"], data["light"]])
        dashboard.update_plot(y_vecs)


if __name__ == "__main__":
    main()
