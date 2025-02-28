import subprocess
import json
import math

odas_process = subprocess.Popen(["/home/rpi/odas/build/bin/odaslive", "-c", "./custom.cfg"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
parsed_data_x = []
x_av=0
parsed_data_y = []
y_av=0
parsed_data_activity = []
ac_av=0
counter = 0


def average(array:list[float])->float:
    av=0
    for i in array:
        av+=i
    return av/len(array)
        

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
        angle = math.atan(x_av/y_av)
        print(f"x={x_av}, y={y_av}, activity={ac_av}, angle={angle}")
        counter = 0
        parsed_data_activity.clear()
        parsed_data_x.clear()
        parsed_data_y.clear()
        
        
