from representation.Device.MetaType import BaseType


class AC(BaseType):
    AC_on = 0

    def __init__(self, func):
        super().__init__()
        self.func = func

    def enable_on(self):
        if self.AC_on == 1:
            return 0
        else:
            return 1

    def action_on(self):
        assert self.AC_on == 0
        self.func()
        self.AC_on = 1

    def enable_off(self):
        if self.AC_on == 0:
            return 0
        else:
            return 1

    def action_off(self):
        assert self.AC_on == 1
        self.AC_on = 0

    def ap_on(self):
        return self.AC_on
