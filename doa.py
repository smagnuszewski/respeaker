import subprocess
import sys
import signal
from pathlib import Path
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
        
def main(odas_process: subprocess):
    
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
        
        light_four(led,ids,angles)
        ids.clear()
        angles.clear()
        counter = 0
        print("---")

        
if __name__ == '__main__':
    try:
        odas_path = Path(sys.argv[1]).resolve().as_posix()
        config_path = Path(sys.argv[2]).resolve().as_posix()
        odas_process = subprocess.Popen([odas_path, "-c", config_path],stdout=subprocess.PIPE, stderr=subprocess.STDOUT,text=True)
        main(odas_process)
    except KeyboardInterrupt:
        print ('Interrupted, turning off audio device...')
        stop_leds(led,5)
        odas_process.send_signal(signal.SIGINT)  # send Ctrl+C to odas
        odas_process.wait()
    finally:
        odas_process.terminate()
        try:
            odas_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            odas_process.kill()
            print("Bad termination")

        sys.exit(0)
