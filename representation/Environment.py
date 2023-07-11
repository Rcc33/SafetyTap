from representation.Space import MeetingRoom, Outer
class Environment(object):
    def __init__(self):
        meeting_room = MeetingRoom()
        outer = Outer()
        self.space_dict = dict()
        self.space_dict["MeetingRoom"] = meeting_room
        self.space_dict["Outer"] = outer
