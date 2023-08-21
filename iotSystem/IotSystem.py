import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
sys.path.append(BASE_DIR)
from copy import deepcopy
import ts.TransitionSystem as TransitionSystem

def _label_generator(space_dict):
    label = []
    for room_name, room in sorted(space_dict.items()):
        for device_name, device in sorted(room["device_dict"].items()):
            for ap_name, ap in sorted(device.ap_dict.items()):
                label = label + [
                    str(room["ap_dict"][room_name + '.' + device_name + '.' + ap_name](device))]
        for name, value in sorted(room["env_state"].items()):
            for ap_name, ap in sorted(value.ap_dict.items()):
                label = label + [
                    str(room["ap_dict"][room_name + '.' + name + '.' + ap_name](value))]
    return label

def get_dict(space_name, space):
    temp  = dict()
    temp["action_dict"] = dict()
    temp["enable_dict"] = dict()
    temp["ap_dict"] = dict()
    temp["state_dict"] = dict()
    temp["ext_action_list"] = list()
    for key, value in space["device_dict"].items():
        for k, v in value.action_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["action_dict"][name] = v
        for k, v in value.enable_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["enable_dict"][name] = v
        for k, v in value.ap_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["ap_dict"][name] = v
        for k, v in value.state_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["state_dict"][name] = v
        for item in value.ext_action_list:
            temp["ext_action_list"].append(space_name + '.' + key + '.' + item)
    for key, value in space["env_state"].items():
        for k, v in value.action_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["action_dict"][name] = v
        for k, v in value.enable_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["enable_dict"][name] = v
        for k, v in value.ap_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["ap_dict"][name] = v
        for k, v in value.state_dict.items():
            name = space_name + '.' + key + '.' + k
            temp["state_dict"][name] = v
        for item in value.ext_action_list:
            temp["ext_action_list"].append(space_name + '.' + key + '.' + item)
    return temp

def _get_field(space_name,space):
    temp = get_dict(space_name,space)
    state_list = [item[1] for item in temp["state_dict"].items()]
    return state_list

def _get_fields(space_dict):
    field = []
    rooms = [item[0] for item in sorted(space_dict.items())]
    state_list = [_get_field(space,space_dict[space]) for space in rooms]
    for s in state_list:
        field = field + s
    return field


def _description_generator(space_dict):
    description = ''
    for room_name, room in space_dict.items():
        for state_name, state_value in room["state_dict"].items():
            description = description + '%s=%s, ' % (state_name, str(state_value))
    description = description[:-2]
    return description


def _apply_action(space_dict, action, act_type):
    (room_name, device_name, action_name) = action.split('.')
    temp = dict()
    for k, v in sorted(space_dict.items()):
        temp[k] = deepcopy(v)
    if room_name not in temp:
        raise Exception('Unfound room %s' % room_name)
    if action not in temp[room_name]["action_dict"]:
        raise Exception('Unfound action %s in room %s' % (action, room_name))
    if act_type == 'device':
        temp[room_name]["action_dict"][action](temp[room_name]["device_dict"][device_name])
        return temp
    if act_type == 'state':
        temp[room_name]["action_dict"][action](temp[room_name]["env_state"][device_name])
    return temp

class IoTSystem(object):
    def __init__(self, environment):
        self.transition_system = None
        self.space_dict = environment["space_dict"]
        self._create_ts()

    def _create_ts(self):
        ap_list = self.getAllAp()
        self.transition_system = TransitionSystem.TS(ap_list)
        field_init = _get_fields(self.space_dict)
        description_init = _description_generator(self.space_dict)
        state_init = TransitionSystem.State(field_init, description_init)
        init_label = _label_generator(self.space_dict)
        init_index = self.transition_system.addState(state_init, init_label)
        state_init_t = (init_index, state_init)
        self._BFS(state_init_t)

    def _BFS(self, state_init_t):
        search_pool = [
            (state_init_t, self.space_dict)]
        while search_pool:
            (state_t, temp_space) = search_pool.pop()
            for room_name, room in sorted(temp_space.items()):
                for device_name, device in sorted(room["device_dict"].items()):
                    for action_name, action in device.action_dict.items():
                        if temp_space[room_name]["enable_dict"][room_name + '.' + device_name + '.' + action_name](device):
                            _get_fields(temp_space)
                            temp = _apply_action(temp_space, room_name + '.' + device_name + '.' + action_name, 'device')
                            new_field = _get_fields(temp)
                            new_description = _description_generator(temp)
                            new_state = TransitionSystem.State(new_field, new_description)
                            new_label = _label_generator(temp)
                            action_description = room_name + '.' + device_name + '.' + action_name
                            if not self.transition_system.ifStateExists(new_state):
                                new_index = self.transition_system.addState(new_state, new_label)
                                search_pool.append(((new_index, new_state), temp))
                            else:
                                new_index = self.transition_system.getIndex(new_field)
                            new_trans = TransitionSystem.Transition(state_t[0], action_description, new_index)
                            if not self.transition_system.ifActionExists(action_description):
                                self.transition_system.addAction(action_description)
                            self.transition_system.addTrans(new_trans)
                for state_name, state in sorted(room["env_state"].items()):
                    for action_name, action in state.action_dict.items():
                        if temp_space[room_name]["enable_dict"][room_name + '.' + state_name + '.' + action_name](state):
                            temp = _apply_action(temp_space, room_name + '.' + state_name + '.' + action_name, 'state')
                            new_field = _get_fields(temp)
                            new_description = _description_generator(temp)
                            new_state = TransitionSystem.State(new_field, new_description)
                            new_label = _label_generator(temp)
                            action_description = room_name + '.' + state_name + '.' + action_name
                            if not self.transition_system.ifStateExists(new_state):
                                new_index = self.transition_system.addState(new_state, new_label)
                                search_pool.append(((new_index, new_state), temp))
                            else:
                                new_index = self.transition_system.getIndex(new_field)
                            new_trans = TransitionSystem.Transition(state_t[0], action_description, new_index)
                            if not self.transition_system.ifActionExists(action_description):
                                self.transition_system.addAction(action_description)
                            self.transition_system.addTrans(new_trans)

    def getAllAp(self):
        ap_list = list()
        for room_name, room in sorted(self.space_dict.items()):
            for key, value in sorted(room["ap_dict"].items()):
                ap_list.append(key)
        return ap_list
