""" Demo a MIDI roundtrip: Keyboard into python into Logic

This script listens for MIDI input on a USB MIDI interface, and when a note is
detected, it creates a major chord arpeggio and plays it back on a virtual MIDI
output port.  Just having Logic open, it picks up those MIDI events.

"""

import random
import time

import mido

MIDI_INPUT = "USB Uno MIDI Interface"

# Set up MIDI input and output ports
mido.set_backend("mido.backends.rtmidi")
midi_in = mido.open_input(MIDI_INPUT)
midi_out = mido.open_output("python_virt_out", virtual=True)


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


# Main loop
try:
    while True:
        print("Listening for MIDI input...")
        for msg in midi_in.iter_pending():
            if msg.type == "note_on":
                print("received note on")
                arpeggio = create_major_arpeggio(msg.note)
                play_arpeggio(arpeggio, midi_out)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    midi_in.close()
    midi_out.close()
