import subprocess
import json
import math
from leds import start_leds, stop_leds, light
import time
import sys


led=start_leds(5)


def average(array:list[float])->float:
    av=0
    for i in array:
        av+=i
    return av/len(array)

        
def main():
    odas_process = subprocess.Popen(["/home/rpi/odas/build/bin/odaslive", "-c", "./custom.cfg"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    parsed_data_x = []
    x_av=0
    parsed_data_y = []
    y_av=0
    parsed_data_activity = []
    ac_av=0
    counter = 0

    while True:
        line = odas_process.stdout.readline()
        line = line.strip()
        if not line:
            continue
        # print(line)
        if line.startswith("{"):
            l = line.removesuffix(",")
            # print(line)
            try:
                data = json.loads(l)
                if data['id']!=0:
                    parsed_data_x.append(data['x'])
                    parsed_data_y.append(data['y'])
                    parsed_data_activity.append(data['activity'])
                    counter = counter + 1        
                # print(data)
            except json.JSONDecodeError as e:
                pass
                # print(f"Error parsing JSON: {e}")
        if counter>=99:
            x_av=average(parsed_data_x)
            y_av=average(parsed_data_y)
            ac_av=average(parsed_data_activity)
            angle = math.degrees(math.atan2(y_av,x_av))+180
            print(f"x={x_av}, y={y_av}, activity={ac_av}, angle={angle}")
            light(strip=led,angle=angle)
            counter = 0
            parsed_data_activity.clear()
            parsed_data_x.clear()
            parsed_data_y.clear()
        
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        stop_leds(led,5)
        print ('interrupted, turning off')
        time.sleep(1)
        sys.exit(0)
