from representation.Device.AC import AC
from representation.Device.Window import Window
from representation.State import Temper

class Space(object):

    def __init__(self):
        self.device_dict = dict()
        self.env_state = dict()
        self.action_dict = dict()
        self.enable_dict = dict()
        self.ap_dict = dict()
        self.state_dict = dict()
        self.ext_action_list = list()


    def get_dict(self, class_name):
        for key, value in self.device_dict.items():
            for k, v in value.action_dict.items():
                name = class_name + '.' + key + '.' + k
                self.action_dict[name] = v
            for k, v in value.enable_dict.items():
                name = class_name + '.' + key + '.' + k
                self.enable_dict[name] = v
            for k, v in value.ap_dict.items():
                name = class_name + '.' + key + '.' + k
                self.ap_dict[name] = v
            for k, v in value.state_dict.items():
                name = class_name + '.' + key + '.' + k
                self.state_dict[name] = v
            for item in value.ext_action_list:
                self.ext_action_list.append(class_name + '.' + key + '.' + item)
        for key, value in self.env_state.items():
            for k, v in value.action_dict.items():
                name = class_name + '.' + key + '.' + k
                self.action_dict[name] = v
            for k, v in value.enable_dict.items():
                name = class_name + '.' + key + '.' + k
                self.enable_dict[name] = v
            for k, v in value.ap_dict.items():
                name = class_name + '.' + key + '.' + k
                self.ap_dict[name] = v
            for k, v in value.state_dict.items():
                name = class_name + '.' + key + '.' + k
                self.state_dict[name] = v
            for item in value.ext_action_list:
                self.ext_action_list.append(class_name + '.' + key + '.' + item)



class MeetingRoom(Space):
    def __init__(self):
        super().__init__()
        temper = Temper()
        self.env_state['temperature'] = temper
        self.device_dict['AC'] = AC(self.event_temper_lower)
        self.device_dict['Window'] = Window()
        self.get_dict('MeetingRoom')

    def get_field(self):
        self.get_dict('MeetingRoom')
        state_list = [item[1] for item in self.state_dict.items()]
        return state_list

    def set_state(self, state):
        self.env_state = state


    def event_temper_higher(self):
        if self.env_state['temperature'].enable_higher(self.env_state['temperature']):
            self.env_state['temperature'].ext_action_higher(self.env_state['temperature'])


    def event_temper_lower(self):
        if self.env_state['temperature'].enable_lower(self.env_state['temperature']):
            self.env_state['temperature'].ext_action_lower(self.env_state['temperature'])

class Outer(Space):

    def __init__(self):
        super().__init__()
        temper = Temper()
        self.env_state['temperature'] = temper
        self.get_dict('Outer')

    def get_field(self):
        self.get_dict('Outer')
        state_list = [item[1] for item in self.state_dict.items()]
        return state_list

    def set_state(self, state):
        self.env_state = state

    def event_temper_higher(self):
        if self.env_state['temperature'].enable_higher(self.env_state['temperature']):
            self.env_state['temperature'].ext_action_higher(self.env_state['temperature'])

    def event_temper_lower(self):
        if self.env_state['temperature'].enable_lower(self.env_state['temperature']):
            self.env_state['temperature'].ext_action_lower(self.env_state['temperature'])
