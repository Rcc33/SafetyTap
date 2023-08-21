from representation.Device.MetaType import BaseType
import requests

class Window(BaseType):
    on = 0

    def __init__(self, state,room):
        super().__init__()
        self.state = state
        self.room = room

    def enable_on(self):
        if self.on == 1:
            return 0
        else:
            return 1

    def action_on(self):
        assert self.on == 0
        url = "http://10.177.29.226:5002/action_info/" + self.room + "/Window/action_on"
        action = requests.get(url).json()
        # 判断pre-conditions，产生相应的effects
        if action["pre_condition"] == "State.Temperature > Room.Temperature":
            room_temper = requests.get("http://10.177.29.226:5002/room_state_info/"  + self.room+ "/Temperature").json()
            outer_temper = requests.get("http://10.177.29.226:5002/room_state_info/Outer/Temperature").json()
            if room_temper["value"] - outer_temper["value"] > 10:
                if self.state.enable_lower(self.state):
                    self.state.ext_action_lower(self.state)
            elif outer_temper["value"] - room_temper["value"] > 10:
                if self.state.enable_higher(self.state):
                    self.state.ext_action_higher(self.state)
        self.on = 1

    def enable_off(self):
        if self.on == 0:
            return 0
        else:
            return 1

    def action_off(self):
        assert self.on == 1
        self.on = 0

    def ap_on(self):
        return self.on
