import os
from buchi.Buchi import Buchi
from iotSystem.IotSystem import IoTSystem
from representation.Environment import Environment

if __name__ == '__main__':
    environment = Environment()
    iot_system = IoTSystem(environment)

    ts = iot_system.transition_system
    buchi_ts = Buchi.ts_to_genbuchi(ts)
    buchi_ltl = Buchi.ltl_to_buchi('F (MeetingRoom.Window.open & MeetingRoom.AC.on)') 
    (buchi_final, pairs) = Buchi.product(buchi_ts, buchi_ltl)

    os.chdir("/home/rjl/SaftyTap")
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
    buchi_final.printToGv(group)

