# Arduino Weather Shield Data-Recorder

Author: Abhishek Anil Deshmukh (deshmukhabhishek369@gmail.com)

Just a python script which
- Stores the data Arduino Weather Shield setup live into a file (`YYYY-MM-DD HH_MM_SS.csv`) with time stamps.
- Shows a dashboard with a plot which shows the values of the input for the last 100 seconds.

## Get the Arduino Weather Shield Running

You can use the script in `Weather_Shield_Basic`. [Link]()

## Quick Start

- Download for: [Windows]()
- Copy contents from [`AWSDRconfig.ini`]() into a file names config.ini in the same directory as where the application was downloaded.
- Set the correct port in `AWSDRconfig.ini`. (`python -m serial.tools.list_ports` to list ports, but you will have to install `pyserial`)

## If you want finer control

- Clone this repository
- Activate a python virtual environment. (Optional + Recommended)
- Install the dependencies `pip install -r requirements.txt`
- Set the correct port in `AWSDRconfig.ini`. (`python -m serial.tools.list_ports` to list ports)
- Run it ` python 'Arduino Weather Shield Data Recorder.py'` 