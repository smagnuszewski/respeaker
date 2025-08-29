import subprocess
import json
from leds import start_leds, stop_leds, light_four
import time
import sys
from frame_parser import Signal

led=start_leds(5)

def get_frame(process: subprocess) -> str:
    frame = '{'
    while True: 
        line = process.stdout.readline().strip()
        frame+=line
        if line =='}':
            break
    return json.loads(frame)
        
def main():
    odas_process = subprocess.Popen(
        ["odaslive", "-c", "./custom.cfg"],
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        text=True)
    

    counter = 0
    signals = []

    for i in range(4):
        signals.append(Signal())
    
    while True:

        # Unwrap stdout
        line = odas_process.stdout.readline().strip()
        if line != '{':
            continue
        frame = get_frame(odas_process)

        # Dividie each frame to signals
        for i in range(4):
            signals[i].readFrame(frame['src'][i])

        counter+=1

        if counter<10:
            continue
        ids = []
        angles=[]
        for s in signals:
            s.normalize(counter)
            s.getAngle()
            ids.append(s.id)
            angles.append(s.angle)
            print(f"id={s.id}, x={s.x}, y={s.y}, activity={s.activity}, angle={s.angle}")
            s.clear()
        # light(strip=led,angle=s.angle)
        
        light_four(led,ids,angles)
        ids.clear()
        angles.clear()
        counter = 0
        print("---")

        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        stop_leds(led,5)
        print ('interrupted, turning off')
        time.sleep(1)
        sys.exit(0)
