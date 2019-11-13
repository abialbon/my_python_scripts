import json
import datetime
import requests
import sys

URL = 'https://www.firstgroup.com/getNextBus'
stationID = '5820WDB48437'
r = requests.post(url=URL, data={ "stop" : stationID})
data = r.json()

def get_base_time(data):
    time_str = data["fromTraveline"][-5:]
    hours = int(time_str.split(":")[0])
    minutes = int(time_str.split(":")[1])
    return datetime.time(hours, minutes)

def get_bus_data(data):
    temp = []
    for d in data["times"]:
        no = d["ServiceNumber"]
        t = d["Due"].split(":")
        time = datetime.time(int(t[0]), int(t[1]))
        temp.append((no, time))
    temp.sort(key=lambda x: x[1])
    return temp

def get_duration_left_str(base, t):
    td_base = datetime.timedelta(hours=base.hour, minutes=base.minute)
    td_t = datetime.timedelta(hours=t.hour, minutes=t.minute)
    diff = td_t - td_base
    minutes_left = int(diff.seconds / 60)
    return "in " + str(minutes_left) + " mins"

def print_bus_times(data, stop_name, l):
    print("-"*17 + "-"*len(stop_name))
    print(f'Bus timings for: {stop_name}')
    print("-"*17 + "-"*len(stop_name))
    for i in range(l):
        print(f'🚌  {data[i][0]:>2} =>  {data[i][1].strftime("%I:%M")}  ({get_duration_left_str(base_time, data[i][1])})')
    print()

def print_bus_no(data, station_name, n):
    temp = list(filter(lambda c: True if c[0] == n else False, data))
    print_bus_times(temp, station_name, 3)

bus_station = data["stop"]["name"]
bus_data = get_bus_data(data)
base_time = get_base_time(data)

if len(sys.argv) == 2:
    print_bus_no(bus_data, bus_station, sys.argv[1])
else:
    print_bus_times(bus_data, bus_station, 5)