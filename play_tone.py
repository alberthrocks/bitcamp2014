#!/usr/bin/env python
# SoundRXTX v1.0 - receive and transmit data with sound!
# Copyright (C) 2014 Albert Huang, Neil Alberg, and William Heimsmoth
# Portions Copyright (C) 2006-2012 Hubert Pham
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import math
import struct
import pyaudio
import time

audio_rate = 48000

def init():
    audio_rate = 48000
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=audio_rate,
        output=True)
    return (p, stream)

def end(ret):
    end_indv(ret[0], ret[1])

def end_indv(p, stream):
    stream.close()
    p.terminate()

def play_tone(frequency, amplitude, duration, fs, stream):
    N = int(fs / frequency)
    T = int(frequency * duration)  # repeat for T cycles
    dt = 1.0 / fs
    # 1 cycle
    tone = (amplitude * math.sin(2 * math.pi * frequency * n * dt)
            for n in xrange(N))
    # todo: get the format from the stream; this assumes Float32
    data = ''.join(struct.pack('f', samp) for samp in tone)
    for n in xrange(T):
        stream.write(data)

'''
# play the C major scale
scale = [130.8, 146.8, 164.8, 174.6, 195.0, 220.0, 246.9, 261.6]
for tone in scale:
    play_tone(tone, 0.5, 0.75, fs, stream)

# up an octave
for tone in scale[1:]:
    play_tone(2*tone, 0.5, 0.75, fs, stream)
'''

if __name__ == "__main__":
    (p, stream) = init()
    tone_list = [ 800, 1000, 2000, 3000, 6000, 8000 ]
    for tone in tone_list:
        print "Playing %i Hz tone!" % tone
        play_tone(tone, 1.0, 0.75, audio_rate, stream)
        time.sleep(1)



