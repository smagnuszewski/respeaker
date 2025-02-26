import subprocess
# import json
odas_process = subprocess.Popen(["/home/rpi/odas/build/bin/odaslive", "-c", "./custom.cfg"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    line = odas_process.stdout.readline()
    if not line:
        break
    print(line)