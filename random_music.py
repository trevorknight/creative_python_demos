"""Simple script to play some random arpeggios out to a virtual MIDI port.

If Logic is open with a software instrument, it can pick up and play those notes.
"""

import mido
import time
import random

# Set up MIDI input and output ports
mido.set_backend("mido.backends.rtmidi")

# Define function to create major chord arpeggio
def create_major_arpeggio(root_note):
    major_third = root_note + 4
    perfect_fifth = root_note + 7
    return [root_note, major_third, perfect_fifth]


# Define function to send arpeggio as MIDI messages
def play_arpeggio(arpeggio, midi_out, duration=0.5):
    for note in arpeggio:
        midi_out.send(mido.Message("note_on", note=note, velocity=64))
        time.sleep(duration)
        midi_out.send(mido.Message("note_off", note=note, velocity=64))

with mido.open_output("python_virt_port", virtual=True) as p:
    time.sleep(2)
    for i in range(10):
        note = random.randint(40, 60)
        arpeg = create_major_arpeggio(note)
        play_arpeggio(arpeg, p)