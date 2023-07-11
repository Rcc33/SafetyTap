from representation.Device.MetaType import BaseType


class Window(BaseType):
    on = 0

    def __init__(self):
        super().__init__()

    def enable_on(self):
        if self.on == 1:
            return 0
        else:
            return 1

    def action_on(self):
        assert self.on == 0
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
