import os
import sys
from representation.Device.AC import AC
from representation.Device.Window import Window
from representation.state.illumination import Illumination

from representation.state.temperature import Temper
BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import buchi.Buchi as Buchi
import requests
from iotSystem.IotSystem import IoTSystem, get_dict

def _getEnvonment():
    env = dict()
    space_dict = dict()

    url = "http://10.177.29.226:5002/room_list" 
    room_list = requests.get(url).json()
    for room in room_list:
        device_dict = dict()
        env_state = dict()
        url = "http://10.177.29.226:5002/device_list/" + room["name"] 
        device_list = requests.get(url).json()
        temper = Temper(room["name"])
        for device in device_list:
            match device["name"]:
                case "AC":
                    device_dict["AC"] = AC(temper, room["name"])
                case "Window":
                    device_dict["Window"] = Window(temper,room["name"])

        url = "http://10.177.29.226:5002/room_state/" + room["name"] 
        room_state = requests.get(url).json()
        for state in room_state:
            match state["name"]:
                case "Temperature":
                    env_state["temperature"] = temper
                case "Illumination":
                    env_state["illumination"] = Illumination(room["name"])
        room_temp = dict()
        room_temp["device_dict"] = device_dict
        room_temp["env_state"] = env_state

        temp = get_dict(room["name"], room_temp)
        room_temp["action_dict"] = temp["action_dict"]
        room_temp["enable_dict"] = temp["enable_dict"]
        room_temp["ap_dict"] = temp["ap_dict"]
        room_temp["state_dict"] = temp["state_dict"]
        room_temp["ext_action_list"] = temp["ext_action_list"]
        space_dict[room["name"]] = room_temp

    env["space_dict"] = space_dict    
    return env

if __name__ == '__main__':
    # environment = Environment()
    # iot_system = IoTSystem(environment)

    environment = _getEnvonment()
    iot_system = IoTSystem(environment)

    ts = iot_system.transition_system
    buchi_ts = Buchi.ts_to_genbuchi(ts)
    buchi_ltl = Buchi.ltl_to_buchi('F (MeetingRoom.Window.on & MeetingRoom.AC.on)') 
    (buchi_final, pairs) = Buchi.product(buchi_ts, buchi_ltl)

    os.chdir("/home/rjl/SafetyTap")
    ts.writeToGv("temp/temp.gv")
    try:   
        os.stat('/temp')
    except FileNotFoundError:
        os.mkdir('/temp')

    buchi_ltl.writeToGv('temp/ltl.gv')
    buchi_ts.writeToGv('temp/ts.gv')
    buchi_final.writeToGv('temp/final.gv')

    # buchi_ts.log()
    # buchi_ltl.log()
    # buchi_final.log()

    group = [s2 for s1, s2 in pairs]

    print()
    # buchi_final.printToGv(group)
    buchi_final.get_safty_specification(ts,pairs)

