from representation.Device.MetaType import BaseType

class Temper(BaseType):
    high = 0
    middle = 1
    low = 0

    def _only_one(*nums):
        count = 0
        for num in nums:
            count += num & 1  # 判断最低位是否为1
            if count > 1:
                return False
        return count == 1

    def enable_lower(self):
        assert self._only_one(self.high,self.middle,self.low)
        if self.low == 1:
            return 0
        else:
            return 1

    def enable_higher(self):
        assert self._only_one(self.high,self.middle,self.low)
        if self.high == 1:
            return 0
        else:
            return 1

    def ext_action_lower(self):
        assert self._only_one(self.high,self.middle,self.low)
        if self.high == 1:
            self.high = 0
            self.middle = 1
            self.low = 0
        elif self.middle == 1:
            self.high = 0
            self.middle = 0
            self.low = 1
        elif self.low == 1:
            return

    def ext_action_higher(self):
        assert self._only_one(self.high,self.middle,self.low)
        if self.high == 1:
            return
        elif self.middle == 1:
            self.high = 1
            self.middle = 0
            self.low = 0
        elif self.low == 1:
            self.high = 0
            self.middle = 1
            self.low = 0

    def ap_high(self):
        return self.high
        
    def ap_middle(self):
        return self.middle

    def ap_low(self):
        return self.low
