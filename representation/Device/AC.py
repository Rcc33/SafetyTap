from representation.Device.MetaType import BaseType
import requests

class AC(BaseType):
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
        url = "http://10.177.29.226:5002/action_info/" + self.room + "/AC/action_on"
        action = requests.get(url).json()
        # 判断pre-conditions，产生相应的effects
        if action["pre_condition"] == '':
            if self.state.enable_lower(self.state):
               self.state.ext_action_lower(self.state)
        self.on = 1

    def enable_off(self):
        if self.on == 0:
            return 0
        else:
            return 1

    def action_off(self):
        assert self.on == 1
        url = "http://10.177.29.226:5002/action_info/" + self.room + "/AC/action_off"
        action = requests.get(url).json()
        # 判断pre-conditions，产生相应的effects
        #if action["pre_condition"] == '':
            # TODO
        self.on = 0

    def ap_on(self):
        return self.on
