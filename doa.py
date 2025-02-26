import subprocess
import json

odas_process = subprocess.Popen(["/home/rpi/odas/build/bin/odaslive", "-c", "./custom.cfg"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
parsed_data = []
counter = 0

while True:
    line = odas_process.stdout.readline()
    line = line.strip()
    if not line:
        continue
    print(line)
    if line.startswith("{"):
        l = line.removesuffix(",")
        # print(line)
        try:
            data = json.loads(l)
            # print(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")