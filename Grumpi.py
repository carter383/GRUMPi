import asyncio
from kasa import SmartPlug
from time import sleep
import pigpio
from time import sleep
import os

pin = 12
PI = pigpio.pi()
positionsMicro= [2300, 1800, 1300, 850, 500]
triggervolts = 240
triggeramps = 2
IP = '<SMART PLUGS IP>'
triggerwatts = triggervolts * triggeramps
triggermilliwatts = triggerwatts * 1000
plug = SmartPlug(IP)
GrumpiState = 5
counter = 450
hour = 3600
hourtime = hour
async def main(plug):
    if plug.is_on == True:
        energyusage =  energyusage = await plug.get_emeter_realtime()
    else:
        await plug.turn_on()
        energyusage =  energyusage = await plug.get_emeter_realtime()
    return energyusage

def pingtest(IP):
    online = False
    hostname = IP
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        online = True
    else:
        online = False
    return online
PI.set_servo_pulsewidth(pin ,positionsMicro[2])
if pingtest(IP) == True:
    asyncio.run(plug.update())
    PI.set_servo_pulsewidth(pin ,positionsMicro[GrumpiState[4] ])
else:
    print('plug Offline')
    sleep(5)


while True:
    PI.set_servo_pulsewidth(pin ,positionsMicro[ - 1])
    if pingtest(IP) == True:
        asyncio.run(plug.update())
        energyusage = asyncio.run(main(plug))
        if (energyusage['power_mw'] >= triggermilliwatts ):
            if GrumpiState != 0:
                GrumpiState -= 1
                PI.set_servo_pulsewidth(pin ,positionsMicro[GrumpiState -1 ])
                sleep(counter)
                houtime = hour
        else:
            if hourtime == 0:
                hourtime = hour
                if GrumpiState != 5:
                    GrumpiState += 1
                    PI.set_servo_pulsewidth(pin ,positionsMicro[GrumpiState -1 ])
            else:
                hourtime -= 5
                sleep(5)
    else:
        print('plug Offline')
        sleep(5)
