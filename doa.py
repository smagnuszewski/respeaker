import subprocess
import json
import math
from leds import start_leds, stop_leds, light
import time
import sys


led=start_leds(5)


def average(array)->list[float]:
    av=[0,0,0,0]
    for i in array:
        av+=i
    return av/len(array)

        
def main():
    # Catch stdout
    odas_process = subprocess.Popen(["/home/rpi/odas/build/bin/odaslive", "-c", "./custom.cfg"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    parsed_data_x = []*4
    x_av=[]
    parsed_data_y = []*4
    y_av=[]
    parsed_data_activity = []*4
    ac_av=[]
    counter = 0
    data_line=[]
    temp=[]
    while True:
        line = odas_process.stdout.readline()
        line = line.strip()
        if not line:
            continue
        if line.startswith('"src"'):
            try:
                # Catches data frame of 4 lines containing loc data and parses it to matrices
                for i in range (4):
                    data_line[i] = odas_process.stdout.readline().removesuffix(",").strip()
                    temp[i] = json.loads(data_line[i])
                    if temp[i]['id']!=0:
                        parsed_data_x[i].append(temp[i]['x'])
                        parsed_data_y[i].append(temp[i]['y'])
                        parsed_data_activity[i].append(temp[i]['activity'])
                counter = counter + 1        
            except json.JSONDecodeError as e:
                pass
                # print(f"Error parsing JSON: {e}")
        if counter>=99:
            x_av=average(parsed_data_x)
            y_av=average(parsed_data_y)
            ac_av=average(parsed_data_activity)
            angle = math.degrees(math.atan2(y_av,x_av))+180
            # print(f"x={x_av}, y={y_av}, activity={ac_av}, angle={angle}")
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
