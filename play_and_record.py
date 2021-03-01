""""
To play and record.
"""
import signals
import subprocess
import re
import json
import argparse 
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from chirp2ir import chirp2ir

## Arguemnts ##
parser = argparse.ArgumentParser()
parser.add_argument("--filename", default="test", help="filename, without file extension", type=str)
parser.add_argument("--format", default="wav", help="audio format", type=str)
parser.add_argument("--signal", default="chirp.wav", help="reference signal", type=str)
parser.add_argument("--impulse", default=0, help="if want to caluclate impulse response", type=bool)
parser.add_argument("--inspect", default=0, help="if want visual inspect signal", type=bool)
args = parser.parse_args()
## Signal to play ##
#ref_sig, fs = sf.readd(parser.signal)
fs = 64000
ref_sig = signals.linear_sweep(T=1, fs=fs, f_lo=150, f_hi=2000, fade=0.1)

## Call for record stream and play signals ##
output = subprocess.check_output('falconpycli').decode('utf-8')
m = json.loads(re.search(r'{.+}', output).group(0).replace("'", '"'))
ipv4 = m['ipv4']
cmd = f"gst-launch-1.0 rtspsrc port-range=5000-5100 location=rtsp://{ipv4}:554/main-audio latency=0 ! decodebin ! audioconvert ! wavenc ! filesink location={args.filename}.{args.format}"

p1 = subprocess.Popen(cmd, shell=True)
sd.play(ref_sig, fs, blocking=True)
p1.terminate()

if args.impulse:
    measured_sig, fs = sf.read(argparse.filename + ".wav")
    chirp2ir(measured_sig, ref_sig, fs, window=True, f_low=150, f_high=8000) # important to remove lower freq to remove dc-bias...

if args.inspect:
    if impulse:
        fig, ax = plt.subplot(3)
        ax[2].plt(ir, title='Calculated IR')
    else:
        fig, ax = plt.subplot(2)
    ax[0].plt(ref_sig, title='Reference Signal')
    ax[1].plt(measured_sig, title='Measured Signal')
    

